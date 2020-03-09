import shutil
print("We r going to now reset all data")
md=['dataset','trainer']
for i in range(2):
	try: shutil.rmtree(md[i])
	except : pass
f=open("id.txt","w+")
f.write("0\n\n")
f.close()
print("Data has been resetted Successfully")


