#include <bits/stdc++.h> 
using namespace std; 
 

struct bucket
 { 
	int data; 
   bucket* link; 
   };
    
struct bucket* top; 
 
void push(int data) 
{  
	struct bucket* temp; 
	temp = new bucket(); 

	if (!temp) { 
		cout << "\nHeap Overflow"; 
		exit(1); 
	} 

	temp->data = data; 

	temp->link = top; 

	top = temp; 
} 
 
int isEmpty() 
{ 
	return top == NULL; 
} 
 
int peek() 
{ 
	 
	if (!isEmpty()) 
		return top->data; 
	else
		exit(1); 
} 


void bpop() 
{ 
	struct bucket* temp; 

	
	if (top == NULL) { 
		cout << "\nStack Underflow" << endl; 
		exit(1); 
	} 
	else { 
		
		temp = top; 
		top = top->link;  
		temp->link = NULL; 
		
		// release memory of top node 
		free(temp); 
		
	}
		cout<<"Your Trolli No is :"<<top->data<<endl; 
    	cout<<"                  ___"<<endl;
	    cout<<"                 /  |"<<endl;
	    cout<<"  ______________/   --"<<endl;
	    cout<<" |___/__ /___/_|     "<<endl;     
	    cout<<" |__/___/___/__|     "<<endl;     
	    cout<<" |_/___/___/___|     "<<endl;     
	    cout<<"    _______/         "<<endl;
	    cout<<"     O   O           "<<endl;


} 

void bdisplay() 
{ 
	struct bucket* temp; 

	 
	if (top == NULL) { 
		cout << "\nStack Underflow"; 
		exit(1); 
	} 
	else { 
		temp = top; 
		while (temp != NULL)
 { 
	cout << temp->data << " ";  
			temp = temp->link; 
		} 
	} 
} 




//int main() {
//   int ch, val; 
//   cout<<"1) Push in stack"<<endl;
//   cout<<"2) Pop from stack"<<endl;
//   cout<<"3) Display stack"<<endl;
//   cout<<"4) Peek stack"<<endl;
//   cout<<"5) Exit"<<endl;
//   do {
//      cout<<"\nEnter choice: "<<endl;
//      cin>>ch;
//      switch(ch) {
//         case 1: {   
//            cout<<"Enter value to be pushed:"<<endl;
//            cin>>val;
//            push(val);
//            break;
//         }
//         case 2: {
//            pop();
//            break;
//         }
//         case 3: {
//            display();
//            break;
//         }
//         case 4: 
//		 {  
//		     cout<<"\npeek value is "<<peek();
//			break;
//		 }
//         case 5: {
//            cout<<"Exit"<<endl;
//            break;
//         }
//         default: {
//            cout<<"Invalid Choice"<<endl;
//         }
//      }
//   }while(ch!=5); 
//      return 0;
//}  
