# dependencies
# pip install tequila-basic
# pip install qulacs
# potentially needs openfermion downgrade from 1.4.0 to 1.3.0
import tequila as tq
import numpy
import time

def run(n_qubits, n_layers=1, backend="qulacs", samples=10000):
    # some parametrized circuit (taking parameter count and depth proportional to n_qubits)
    # supposed to mimick features of circuits coming from QAOA style time evolutions
    # parameter count: n_layers*n_qubits
    # depth = n_layers*n_qubits + 1
    U = tq.gates.H(target=[i for i in range(n_qubits)])
    for layer in range(n_layers):
        for q in range(n_qubits):
            U += tq.gates.Ry(angle=(q,layer,0), target=q)
        for q in range(0,n_qubits-1):
            U += tq.gates.CNOT(q,q+1%n_qubits)
    
    # make circuit picture
    #U.export_to(filename="circuit_8_1.png")
    
    # QAOA style measurement (standard basis, or all-z Hamiltonian)
    H = tq.paulis.Z([i for i in range(n_qubits)])
    
    # Expectation Value to measure
    E = tq.ExpectationValue(H=H, U=U)

    # single gradient evaluation of random parameter in circuit
    dE = tq.grad(E, variable=numpy.random.choice(E.extract_variables()))
    
    # compile cost and gradient function
    cost = tq.compile(E, backend=backend)
    grad_cost = tq.compile(dE, backend=backend)
            
    # all variables to 1.0 in evaluation
    variables = {k:1.0 for k in E.extract_variables()}
    
    start = time.time()
    evaluated = cost(variables, samples=samples)
    stop = time.time()
    print("{:2} qubits, {:3} layers, {:5} samples/shots : {:3.1f}s for cost function".format(n_qubits, n_layers, str(samples), stop-start))
    time_cost = stop-start
    
    start = time.time()
    evaluated = grad_cost(variables, samples=samples)
    stop = time.time()
    time_grad = stop-start
    print("{:2} qubits, {:3} layers, {:5} samples/shots : {:3.1f}s for gradient".format(n_qubits, n_layers, str(samples), stop-start))
    
    return time_cost, time_grad

####### Create Plots:
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
