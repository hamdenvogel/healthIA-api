
import sys
import time

print("Importing time...")
t0 = time.time()
import pandas
print(f"Pandas imported in {time.time()-t0:.4f}s")

print("Importing cleaningService...")
t0 = time.time()
from services.cleaningService import limpar_texto
print(f"cleaningService imported in {time.time()-t0:.4f}s")

print("Importing datasetService...")
t0 = time.time()
import services.datasetService
print(f"datasetService imported in {time.time()-t0:.4f}s")
