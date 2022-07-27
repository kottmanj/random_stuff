data_cost1 = {}
data_grad1 = {}
for n_qubits in [8,10,12,14,16,18,20,22]: 
    for n_layers in [1]:
        for samples in [10000]:
            x,y=run(n_qubits=n_qubits, n_layers=n_layers, samples=samples, backend="qulacs")
            data_cost1[n_qubits]=x
            data_grad1[n_qubits]=y
            
data_cost2 = {}
data_grad2 = {}
for n_qubits in [8,10,12,14,16]: 
    for n_layers in [100]:
        for samples in [10000]:
            x,y=run(n_qubits=n_qubits, n_layers=n_layers, samples=samples, backend="qulacs")
            data_cost2[n_qubits]=x
            data_grad2[n_qubits]=y
            
data_cost3 = {}
data_grad3 = {}
for n_qubits in [8,10,12,14,16]: 
    for n_layers in [100]:
        for samples in [None]:
            x,y=run(n_qubits=n_qubits, n_layers=n_layers, samples=samples, backend="qulacs")
            data_cost3[n_qubits]=x
            data_grad3[n_qubits]=y
            
import matplotlib.pyplot as plt

x1 = list(data_cost1.keys())
tc1 = list(data_cost1.values())
tg1 = list(data_grad1.values())

x2 = list(data_cost2.keys())
tc2 = list(data_cost2.values())
tg2 = list(data_grad2.values())

x3 = list(data_cost3.keys())
tc3 = list(data_cost3.values())
tg3 = list(data_grad3.values())

plt.title("SKD: tequila, backend: qulacs, 10.000 samples/shots")
plt.plot(x1,tc1,label="cost (depth=4)")
plt.plot(x1,tg1,label="grad (depth=4)")
plt.plot(x2,tc2,label="cost (depth=301)")
plt.plot(x2,tg2,label="grad (depth=301)")
plt.plot(x3,tc3,label="cost (depth=301) - no-sampling", linestyle="--")
plt.plot(x3,tg3,label="grad (depth=301) - no-sampling", linestyle="--")
plt.xlabel("n_qubits")
plt.ylabel("time/s")
plt.yscale("log")
plt.legend()
plt.savefig("timings_tq_qulacs.png")
plt.show()
