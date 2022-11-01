import matplotlib.pyplot as plt

with open("rewards.txt", "r") as f:
	r = f.readline()[1:-1].split()
	
	for i in range(len(r)):
		r[i] = r[i].replace(',', '')
		
	plt.plot(r, 'b')
	plt.ylabel('reward')
	plt.xlabel('episode')
	plt.yscale('log')
	plt.title('total reward over episodes')
	plt.grid(True)
	plt.show()
