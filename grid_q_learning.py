import numpy as np
from math import *
from random import *
from scene import *
import time


class Environment(Scene):

	def setup(self):
		self.grid_size = 6
		self.squares = np.random.randint(-10, 10, size=(self.grid_size, self.grid_size))
		self.squares[-1, -1] = 20
		#self.squares[randint(0, self.grid_size - 1), randint(0, self.grid_size - 1)] = 1000
		self.background_color = 'white'
		self.length = 100
		self.state_size = self.grid_size**2  # numbers of possible states
		self.action_size = 4  # numbers of actions
		self.gamma = 0.8  # discount factor to balance future and immediate reward
		self.epsilon = 1  # percent of the time when robot explores or exploits
		self.learning_rate = 1
		self.state = 0
		self.timer = 0
		self.Q = np.zeros((self.state_size, self.action_size))  # q table for actions, state, and reward triplets
		self.agent = SpriteNode('typb:User')
		self.agent.position = self.length, self.length
		self.add_child(self.agent)
		self.pos_to_state = {}
		self.epochs = 0
		self.episodes = 0
		self.total_rewards = [0]
		self.total_R = 0
		self.epsilon_decay = 0.99999
		self.epsilon_min = 0
		counter = 0
		for h in range(self.grid_size):
			for k in range(self.grid_size):
				self.pos_to_state[(self.length * h, self.length * k)] = counter
				counter += 1

	def move(self, action):
		pos = self.agent.position
		if action == 0 and self.agent.position.y != self.length * self.grid_size:
			pos.y += self.length
		elif action == 1 and self.agent.position.x != self.length * self.grid_size:
			pos.x += self.length
		elif action == 2 and self.agent.position.y != self.length:
			pos.y -= self.length
		elif action == 3 and self.agent.position.x != self.length:
			pos.x -= self.length
		self.agent.position = pos

	def optimal_action(self):
		possible_rewards = []
		for i in range(4):
			possible_rewards.append(
				self.Q[self.pos_to_state[int(self.agent.position.x - self.length), int(
					self.agent.position.y - self.length)], i])
		for r in range(len(possible_rewards)):
			if possible_rewards[r] == max(possible_rewards):
				return r

	def update_Q(self, new_state, action, reward):
		self.Q[self.state,action] = self.Q[self.state, action] + self.learning_rate * (reward + self.gamma * np.max(self.Q[new_state, :]) - self.Q[self.state, action])
		self.state = new_state

	def episode(self):
		reward = 0
		if self.epochs == self.state_size:
			self.epochs = 0
			self.agent.position = self.length, self.length
			self.episodes += 1
			#self.epsilon -= 0.01
			self.total_rewards.append(self.total_R)
			with open("rewards.txt", "w") as f:
				f.write(str(self.total_rewards))
			self.total_R = 0

		if uniform(0, 1) < self.epsilon:  #explore
			action = randint(0, 3)
			self.step(action)

		else:  # find action that gives highest reward
			action = self.optimal_action()
			self.step(action)

		if self.epsilon > self.epsilon_min:
			self.epsilon *= self.epsilon_decay
		else:
			self.epsilon = self.epsilon_min

	def step(self, action):
		self.move(action)
		reward = self.squares[(self.agent.position.x / self.length) - 1][(self.agent.position.y / self.length) - 1]
		new_state = self.pos_to_state[int(self.agent.position.x - self.length), int(
			self.agent.position.y - self.length)]
		self.update_Q(new_state, action, reward)
		self.total_R += reward
		self.epochs += 1

	def draw(self):
		for i in range(self.grid_size):
			for j in range(self.grid_size):
				if self.squares[i][j] < 0:
					fill('red')
				elif self.squares[i][j] > 0:
					fill('green')
				elif self.squares[i][j] == 0:
					fill('gray')

				font_size = self.length - 40
				rect(
					i * (self.length + 1) + 10,
					j * (self.length + 1) + 10,
					self.length,self.length
				)
				tint('black')
				text(
					str(self.squares[i][j]),
					font_name='Helvetica',
					font_size=font_size,
					x=i * (self.length + 1) + font_size,
					y=j * (self.length + 1) + font_size
				)
				tint('black')
				text(
					"epoch:" + str(self.epochs),
					font_name='Helvetica',
					font_size=50,
					x=800,
					y=500
				)
				text(
					"episode:" + str(self.episodes),
					font_name='Helvetica',
					font_size=50,
					x=800,
					y=450
				)
				text(
					"total reward:" + str(self.total_rewards[self.episodes]),
					font_name='Helvetica',
					font_size=50,
					x=800,
					y=400
				)
				text(
					"epsilon:" + str(self.epsilon),
					font_name='Helevtica',
					font_size=50,
					x=800,
					y=350
				)
				#text("q table:" + str(self.Q), font_name='Helvetica', font_size = 10, x=800, y=200)

		for _ in range(200): self.episode()
		#time.sleep(0.02)
		"""
		if self.timer == 10:
			self.episode()
			self.timer = 0
		else:
			self.timer += 1
		"""

run(Environment(), show_fps=True, frame_interval=1)
