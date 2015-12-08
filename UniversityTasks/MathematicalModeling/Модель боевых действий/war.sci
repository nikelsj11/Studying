a1=0;
a2=0;

b1=0;
b2=0;


function P=P(t)
    P=0;
endfunction

function Q=Q(t)
    Q=0;
endfunction

// =====регулярные войска
//function dy=war(t, NM)
//      dy(1) = -a1*NM(1)-b2*NM(2)+P(t) //N
//      dy(2) = -a2*NM(2)-b1*NM(1)+Q(t) //M
//endfunction

// =====партизанские войска
//function dy=war(t, NM)
//      dy(1) = -a1*NM(1)-b2*NM(2)*NM(1)+P(t) //N
//      dy(2) = -a2*NM(2)-b1*NM(1)*NM(2)+Q(t) //M
//endfunction

// ======регулярные+партизаны
function dy=war(t, NM)
      dy(1) = -a1*NM(1)-b2*NM(2)+P(t); //N
      dy(2) = -a2*NM(2)-b1*NM(1)*NM(2)+Q(t); //M
endfunction

t0=0;

N0M0=[0;0];

flag=1;

clf();

//===============================================================
//============ N - M
if flag==0 then
    t=[0:0:0];
    
    result=ode(N0M0, t0, t, war);
    
    n = size(result, "c");
    
    for i = 1: n-2       
        T(i) = t(i);
        N(i) = result(1, i);
        M(i) = result(2, i); 
        if (result(1, i)<1) then
            N(i) = 0;
            break;
        end
        if (result(2, i)<1) then
            M(i) = 0;
            break;
        end

    end


    xtitle("Модель боевых действий между регулярными отрядами", "Армия M",   "Армия N");

    title("Модель боевых действий между регулярными отрядами","color","red","fontsize",4); 
    
    plot2d4(M, N);
    
    legend(["Динамика изменения численности армий M и N"]);


//===============================================================
//============ N - t | M - t
else if flag==1 then
    t=[0:0:0];
    
    result=ode(N0M0, t0, t, war)
    
    n = size(result, "c")
    
    for i = 1: n-2
        T(i) = t(i);
        if result(1, i)<1 then
            N(i)=0;
        else
            N(i) = result(1, i);
        end
        if result(2, i)<1 then
            M(i)=0;
        else
            M(i) = result(2, i);
        end
    end
    
    xtitle("Модель боевых действий между регулярными отрядами", "Время",   "Численность");

    title("Модель боевых действий между регулярными отрядами","color","red","fontsize",4); 
    
    plot(T, N, 'r');
    plot(T, M, 'b');
    
    legend(["Динамика изменения численности армии N"; 
            "Динамика изменения численности армии M"]);
end
end

xgrid();



