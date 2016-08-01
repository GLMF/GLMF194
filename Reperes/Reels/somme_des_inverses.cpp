#include <stdio.h>
#include <iomanip>
#include <iostream>

float somme(int N){
	float res = 0.0;
  	for (int i=1;i<=N;i++){
		res += (1.0/i);
	}
	std::cout<<"somme de 1 à "<<N<<" : "<<std::setprecision(7)<<res<<std::endl;
	
	res = 0.0;
  	for (int i=N;i>=1;i--){
		res += (1.0/i);
	}
	std::cout<<"somme de "<<N<<" à 1 :"<<std::setprecision(7)<<res<<std::endl<<std::endl;
}

int main(){
	somme(100000); 
	somme(1000000);
	somme(10000000);
	somme(100000000);
	return 0;
}
