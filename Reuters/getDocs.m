a = find(gnd(:) == 9);
fileID = fopen('coffee.txt','w');
fprintf(fileID,'%i\n',a);
fclose(fileID);