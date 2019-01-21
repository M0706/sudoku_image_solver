#include <bits/stdc++.h>
typedef long long ll;
#define v2d std::vector< std::vector<int> >
#define M 9
using namespace std;
ll cnt=0;
v2d mat(9,vector<int>(9,0));
int compute_boxno(int i,int j)
{
	int hor=i/3,ver=j/3;
	return hor*3+ver;
}
struct point{
	int i,j;
	bitset<M> not_possible;
};
void display_solution()
{
	// for(int i=0;i<9;i++)
	// {
	// 	for(int j=0;j<9;j++)
	// 	{
	// 		cout<<mat[i][j]<<" ";
	// 	}
	// 	cout<<endl;
	// }
	// exit(0);
	cout<<cnt++<<endl;
}
struct point extract_vector()
{
	bitset<M> restric_hor[9];
	bitset<M> restric_ver[9];
	bitset<M> restric_box[9];
	int flag=1;
	for(int i=0;i<9;i++)
	{
		for(int j=0;j<9;j++)
		{
			int temp=mat[i][j];
			if(temp) 
			{
				temp--;
				restric_ver[j]|=1<<temp;
				restric_hor[i]|=1<<temp;
				int boxno=compute_boxno(i,j);
				restric_box[boxno]|=1<<temp;
			}
			else flag=0;
		}
	}
	struct point p={-1,-1};
	if(flag){
		display_solution();
		return p;
	}
	int max=-1;
	for(int i=0;i<9;i++)
	{
		for(int j=0;j<9;j++)
		{
			int temp=mat[i][j];
			if(!temp)
			{
				bitset<M> s;
				int boxno=compute_boxno(i,j);
				s=restric_box[boxno]|restric_ver[j]|restric_hor[i];
				int sz=s.count();
				if(sz>max)
				{
					p.i=i;p.j=j;
					p.not_possible=s;
					max=sz;
				}
			}
		}
	}
    return p;
}


void solve_sudoku()
{
	struct point vertex=extract_vector();
	if(vertex.i==-1) return;
	for(int i=0;i<9;i++)
	{
		if(vertex.not_possible[i])
			    continue;
		else
		{
			mat[vertex.i][vertex.j]=i+1;
			solve_sudoku();
			mat[vertex.i][vertex.j]=0;
		}
	}
	return ;		
}

int main()
{
	mat[0][0]=1;
	solve_sudoku();
	return 0;
}