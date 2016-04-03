//alpha1=0.005;
alpha1=0.0008;
alpha2=0.000005;

//alpha2=0;
N=5000;

//gamma_=10;
//N0=N/gamma_;
N0=100;
t_range=[0:0.01:500];


//function alpha1=alpha1(t)
//


alpha1=0.1*sin(t);


//endfunction


function y=y(t, n)
//y=(alpha1(t)+alpha2*x)*(N-x);
y=(alpha1+alpha2*n)*(N-n);
endfunction


x=ode(N0,0,t_range,y);

//нахождение максимальной интенсивности роста числа клиентов
max_t=0;
max_x=0;
max_v=0;
for i=1:(size(x, "c")-1)
max_v_tmp=abs(x(i)-x(i+1));
if (max_v_tmp>max_v) then
max_v=max_v_tmp;
max_t=t_range(i);
max_x=x(i);
end
end

mprintf('Наибольшая интенсивность:\t%5.3f\nN(t):\t%5.3f\nt:\t %5.3f',max_v,max_x, max_t);

plot2d(max_t,max_x,-3);

//находим момент когда компания становится заведомо убыточной
fri_x=1;
fri_t=1;
for i=1:(size(x, "c")-1)
    if (abs(x(i)-N)<0.5) then
    fri_x=x(i);
    fri_t=t_range(i);
    break;
    end
end

plot2d(fri_t,fri_x,-2);
plot(t_range,x, 'r');
xgrid();






