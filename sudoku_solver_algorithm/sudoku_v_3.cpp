#include <bits/stdc++.h>
typedef long long ll;
#define v2d std::vector< std::vector<int> >
#define M 9
using namespace std;
ll cnt=0;
v2d mat(9,vector<int>(9,0));
bitset<M> restric_hor[9]={};
bitset<M> restric_ver[9]={};
bitset<M> restric_box[9]={};

int compute_boxno(int i,int j)
{
	int hor=i/3,ver=j/3;
	return hor*3+ver;
}
void add_entry(int x,int y,int i)
{
	restric_ver[x]|=1<<i;
	restric_hor[y]|=1<<i;
	int boxno=compute_boxno(y,x);
	restric_box[boxno]|=1<<i;
}
void remove_entry(int x,int y,int i)
{
	int boxno=compute_boxno(y,x);
	restric_ver[x]^=1<<i;
	restric_hor[y]^=1<<i;
	restric_box[boxno]^=1<<i;
	
}
struct point{
	int i,j;
	bitset<M> not_possible;
};
void display_solution()
{
	for(int i=0;i<9;i++)
	{
		for(int j=0;j<9;j++)
		{
			cout<<mat[i][j]<<" ";
		}
		cout<<endl;
	}
	exit(0);
	// cout<<cnt++<<endl;
 // if(cnt>100000) 	exit(0);
}
struct point extract_point()
{
	struct point p;
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
	if(max==-1){
		display_solution();
		p.i=-1;
		return p;
	}
    return p;
}


void solve_sudoku()
{
	struct point vertex=extract_point();
	int x=vertex.j,y=vertex.i;
	if(vertex.i==-1) return;
	for(int i=0;i<9;i++)
	{
		if(vertex.not_possible[i])
			    continue;
		else
		{
			mat[y][x]=i+1;
			add_entry(x,y,i);
			solve_sudoku();
			remove_entry(x,y,i);
		}
	}
	mat[y][x]=0;
	return ;		
}

int main()
{	
	solve_sudoku();
	return 0;
}