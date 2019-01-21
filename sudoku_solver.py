#######   sudoku solving part ############### 
import numpy as np

cnt=0
mat=np.zeros((9,9))

restric_hor = np.zeros(9,np.uint16)
restric_ver = np.zeros(9,np.uint16)
restric_box = np.zeros(9,np.uint16)

def compute_boxno(i,j):
	hor = (i-i%3)/3
	ver = (j-j%3)/3 
	return hor*3+ver 

def add_entry(x,y,i):
	restric_ver[x]|= 1<<i
	restric_hor[y]|= 1<<i 
	boxno = compute_boxno(y,x) 
	restric_box[boxno] |= 1<<i 

def remove_entry(x,y,i):
	boxno=compute_boxno(y,x) 
	restric_ver[x] ^= 1<<i 
	restric_hor[y] ^= 1<<i 
	restric_box[boxno] ^= 1<<i 
  

def display_solution():
	print mat
	exit()

def count(x):
	cnt=0
	while x:
		if x%2 :
			cnt+=1
			x-=1
		x /= 2
	return cnt

def extract_point ():

	point = [0,0]
	s=np.zeros((9,9))
	max=-1 
	for i in range (0,9):
		for j in range (0,9):
			temp=mat[i][j] 
			if temp==0:
				boxno=compute_boxno(i,j) 
				s[i][j]=(restric_box[boxno]|restric_ver[j])|restric_hor[i]
				sz=count(s[i][j]) 
				if(sz>max):
					point = [i,j]
					max=sz 
	if max == -1 :
		display_solution() 
		point[0] = -1 
	return point

def solve_sudoku():
 
	vertex = extract_point() 
	y,x = vertex
	if(y==-1):
		return 
	boxno=compute_boxno(y,x) 
	not_possible = restric_box[boxno]|restric_ver[x]|restric_hor[y]

	for i in range (0,9):
		if (not_possible & 1<<i ):
			continue
		else:
			mat[y][x] = i+1
			add_entry(x,y,i) 
			solve_sudoku() 
			remove_entry(x,y,i)
		 
	mat[y][x]=0 
	return  		

def start_solving(sudoku):
	for i in range (0,9):
		for j in range (0,9):
			if (sudoku[i][j]):
				mat[i][j]=sudoku[i][j]
				add_entry(j,i,int(mat[i][j]-1))

	solve_sudoku()

def main():
	# sudoku=input()
	# print sudoku
	start_solving(mat)

if __name__ == '__main__':
	main()