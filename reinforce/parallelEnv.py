# taken from openai/baseline
# with minor edits
# see https://github.com/openai/baselines/baselines/common/vec_env/subproc_vec_env.py
# 


import numpy as np
import gymnasium as gym
from multiprocessing import Process, Pipe
from abc import ABC, abstractmethod

class CloudpickleWrapper(object):
    """
    Uses cloudpickle to serialize contents (otherwise multiprocessing tries to use pickle)
    """

    def __init__(self, x):
        self.x = x

    def __getstate__(self):
        import cloudpickle
        return cloudpickle.dumps(self.x)

    def __setstate__(self, ob):
        import pickle
        self.x = pickle.loads(ob)

class VecEnv(ABC):
    """
    An abstract asynchronous, vectorized environment.
    """

    def __init__(self, num_envs, observation_space, action_space):
        self.num_envs = num_envs
        self.observation_space = observation_space
        self.action_space = action_space

    @abstractmethod
    def reset(self):
        """
        Reset all the environments and return an array of
        observations, or a dict of observation arrays.
        If step_async is still doing work, that work will
        be cancelled and step_wait() should not be called
        until step_async() is invoked again.
        """
        raise NotImplementedError

    @abstractmethod
    def step_async(self, actions):
        """
        Tell all the environments to start taking a step
        with the given actions.
        Call step_wait() to get the results of the step.
        You should not call this if a step_async run is
        already pending.
        """
        raise NotImplementedError

    @abstractmethod
    def step_wait(self):
        """
        Wait for the step taken with step_async().
        Returns (obs, rews, dones, infos):
         - obs: an array of observations, or a dict of
                arrays of observations.
         - rews: an array of rewards
         - dones: an array of "episode done" booleans
         - infos: a sequence of info objects
        """
        raise NotImplementedError

    @abstractmethod
    def close(self):
        """
        Clean up the environments' resources.
        """
        raise NotImplementedError

    def step(self, actions):
        """
        Step the environments synchronously.
        This is available for backwards compatibility.
        """
        self.step_async(actions)
        return self.step_wait()

    def render(self, mode='human'):
        """Render the environment. Default implementation does nothing."""
        # mode parameter maintained for API compatibility
        return None
        
    @property
    def unwrapped(self):
        """Return the unwrapped environment."""
        return self


def worker(remote, parent_remote, env_fn_wrapper):
    parent_remote.close()
    env = env_fn_wrapper.x
    while True:
        cmd, data = remote.recv()
        if cmd == 'step':
            # Handle modern Gymnasium API (returns 5 values) vs old API (4 values)
            step_result = env.step(data)
            if len(step_result) == 5:
                ob, reward, terminated, truncated, info = step_result
                done = terminated or truncated
            else:
                ob, reward, done, info = step_result
            
            if done:
                # Handle modern Gymnasium reset API that returns (obs, info)
                reset_result = env.reset()
                if isinstance(reset_result, tuple):
                    ob, _ = reset_result
                else:
                    ob = reset_result
            remote.send((ob, reward, done, info))
        elif cmd == 'reset':
            # Handle modern Gymnasium reset API that returns (obs, info)
            reset_result = env.reset()
            if isinstance(reset_result, tuple):
                ob, _ = reset_result
            else:
                ob = reset_result
            remote.send(ob)
        elif cmd == 'reset_task':
            ob = env.reset_task()
            remote.send(ob)
        elif cmd == 'close':
            remote.close()
            break
        elif cmd == 'get_spaces':
            remote.send((env.observation_space, env.action_space))
        else:
            raise NotImplementedError


class parallelEnv(VecEnv):
    def __init__(self, env_name='PongDeterministic-v4',
                 n=4, seed=None):

        # Create environments without using deprecated seed method
        # Note: seed parameter kept for API compatibility but not used (modern Gymnasium approach)
        env_fns = []
        for _ in range(n):
            env = gym.make(env_name)
            env_fns.append(env)
        
        # Note: Seeds are now handled in the reset() method of individual environments
        # Modern Gymnasium doesn't use env.seed() anymore
        
        # envs: list of gym environments to run in subprocesses
        # adopted from openai baseline
        self.waiting = False
        self.closed = False
        nenvs = len(env_fns)
        self.remotes, self.work_remotes = zip(*[Pipe() for _ in range(nenvs)])
        self.ps = [Process(target=worker, args=(work_remote, remote, CloudpickleWrapper(env_fn)))
            for (work_remote, remote, env_fn) in zip(self.work_remotes, self.remotes, env_fns)]
        for p in self.ps:
            p.daemon = True # if the main process crashes, we should not cause things to hang
            p.start()
        for remote in self.work_remotes:
            remote.close()

        self.remotes[0].send(('get_spaces', None))
        observation_space, action_space = self.remotes[0].recv()
        VecEnv.__init__(self, len(env_fns), observation_space, action_space)

    def step_async(self, actions):
        for remote, action in zip(self.remotes, actions):
            remote.send(('step', action))
        self.waiting = True

    def step_wait(self):
        results = [remote.recv() for remote in self.remotes]
        self.waiting = False
        obs, rews, dones, infos = zip(*results)
        return np.stack(obs), np.stack(rews), np.stack(dones), infos

    def reset(self):
        for remote in self.remotes:
            remote.send(('reset', None))
        return np.stack([remote.recv() for remote in self.remotes])

    def reset_task(self):
        for remote in self.remotes:
            remote.send(('reset_task', None))
        return np.stack([remote.recv() for remote in self.remotes])

    def close(self):
        if self.closed:
            return
        if self.waiting:
            for remote in self.remotes:            
                remote.recv()
        for remote in self.remotes:
            remote.send(('close', None))
        for p in self.ps:
            p.join()
        self.closed = True
