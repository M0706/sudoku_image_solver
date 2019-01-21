#include <iostream>
#include <vector>
#include <set>
#include <algorithm>
typedef long long ll;
#define v2d std::vector< std::vector<int> >
#define pb push_back
using namespace std;
ll cnt=0;
int compute_boxno(int i,int j)
{
	int hor=i/3,ver=j/3;
	return hor*3+ver;
}
struct point{
	int i,j;
	set<int> possible;
};
void display_solution(v2d mat)
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
struct point extract_vector(v2d mat)
{
	vector<set<int> > restric_hor(9);
	vector<set<int> > restric_ver(9);
	vector<set<int> > restric_box(9);
	int flag=1;
	for(int i=0;i<9;i++)
	{
		for(int j=0;j<9;j++)
		{
			int temp=mat[i][j];
			if(temp) 
			{
				restric_ver[j].insert(temp);
				restric_hor[i].insert(temp);
				int boxno=compute_boxno(i,j);
				restric_box[boxno].insert(temp);
			}
			else flag=0;
		}
	}
	struct point p={-1,-1};
	if(flag){
		display_solution(mat);
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
				set<int> s;
				for(auto it : restric_hor[i]) s.insert(it);
				for(auto it : restric_ver[j]) s.insert(it);
				int boxno=compute_boxno(i,j);
				for(auto it : restric_box[boxno]) s.insert(it);
				int sz=s.size();
				if(sz>max)
				{
					p.i=i;p.j=j;
					p.possible=s;
					max=sz;
				}
			}
		}
	}
    return p;
}


void solve_sudoku(v2d mat)
{
	struct point vertex=extract_vector(mat);
	if(vertex.i==-1) return;
	set<int>::iterator it=vertex.possible.begin();
	for(int i=1;i<=9;i++)
	{
		if(i== *it)
			{
			    it++;
			    continue;
			}
		else
		{
			mat[vertex.i][vertex.j]=i;
			solve_sudoku(mat);
		}
	}
	return ;		
}

int main()
{
	v2d mat(9,vector<int>(9,0));
	int n;
	// cout<<"Enter total number of inputs:";
	// cin>>n;
	// while(n--)
	// {
	// 	int i,j;
		// cout<<"Enter i:";
	// 	cin>>i;
	// 	// cout<<"Enter j:";
	// 	cin>>j;
	// 	// cout<<"Enter value:";
	// 	cin>>mat[i][j];
	// }
	solve_sudoku(mat);
	return 0;
}