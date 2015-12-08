k=10;

x1=-k;
x2=k;

teta1=0;
teta2=-%pi;

function evaluate=chase(t,r);
    evaluate=r/sqrt(3);
endfunction    


way=1;

scf(1);
clf(1);
title("Задача о погоне","color","red","fontsize",4); 

if way==0 then
    teta = [teta2:0.01:-%pi+8];
    result=ode(x2, teta2, teta, chase);  
    polarplot(teta, result, style=5); 
    
    result_lodka=[0:0.01:310];
    teta_lodka=1.6580627893946;
    polarplot(teta_lodka, result_lodka, style=12);
    
    for i = 1: size(teta, "c")
        a=abs(teta(i)-%pi-teta_lodka);
        
        if (a<0.01) then
            mprintf('\nF=%f\tR=%f\tdiff=%f',teta(i),result(i), a)
        end
    end    
    
else
    teta = [teta1:0.01:%pi+0.5];
    result=ode(x1, teta1, teta, chase);
    polarplot(teta, result, style=6);
    
    result_lodka=[0:0.01:100];
    teta_lodka=0.087266462599716;
    polarplot(teta_lodka, result_lodka, style=12);
    
    for i = 1: size(teta, "c")
        a=abs(teta(i)-%pi-teta_lodka);
        
        if (a<0.01) then
            mprintf('\nF=%f\tR=%f\tdiff=%f',teta(i),result(i), a)
        end
    end
end



legend("Траектория движения катера", "Траектория движения лодки"); 

