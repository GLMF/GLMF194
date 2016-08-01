#include <iomanip>
#include <iostream>
#include <fenv.h>

void affectation(){
	float a;
	std::cout<<"Entrer la valeur de a"<<std::endl;
	std::cin>>a;
	std::cout<<" a : "<<a<<std::endl;
}

int main(){
  std::cout<<std::setprecision(10);
  
  std::cout<<"mode d'arrondi RD"<<std::endl;
  std::cout<<"-----------------"<<std::endl;
  fesetround(FE_DOWNWARD);
  affectation();
	  
  std::cout<<std::endl<<"mode d'arrondi RU"<<std::endl;
  std::cout<<"-----------------"<<std::endl;
  fesetround(FE_UPWARD);
  affectation();
  
  std::cout<<std::endl<<"mode RN"<<std::endl;
  std::cout<<"-------"<<std::endl;
  fesetround(FE_TONEAREST);
  affectation();

  return 0;
}