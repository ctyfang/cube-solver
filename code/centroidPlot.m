blue = csvread('bluPix.csv');
bCent = mean(blue,1)

red = csvread('redPix.csv');
rCent = mean(red,1)

green = csvread('grnPix.csv');
gCent = mean(green,1)

orange = csvread('oraPix.csv');
oCent = mean(orange,1)

white = csvread('whtPix.csv');
wCent = mean(white,1)

yellow = csvread('ylwPix.csv');
yCent = mean(yellow,1)

scatter3(blue(:,1),blue(:,2),blue(:,3),[],[0,0,1])
hold on;
scatter3(bCent(:,1),bCent(:,2),bCent(:,3),30,[1,1,1],'filled')

scatter3(red(:,1),red(:,2),red(:,3),[],[1,0,0])
scatter3(rCent(:,1),rCent(:,2),rCent(:,3),30,[1,0,0])

scatter3(green(:,1),green(:,2),green(:,3),[],[0,1,0])
scatter3(gCent(:,1),gCent(:,2),gCent(:,3),30,[0,1,0])

scatter3(orange(:,1),orange(:,2),orange(:,3),[],[1 0.25 0])
scatter3(oCent(:,1),oCent(:,2),oCent(:,3),30,[1 0.25 0])

scatter3(white(:,1),white(:,2),white(:,3),[],[0 0 0])
scatter3(wCent(:,1),wCent(:,2),wCent(:,3),30,[0 0 0])

scatter3(yellow(:,1),yellow(:,2),yellow(:,3),[],[1 1 0])
scatter3(yCent(:,1),yCent(:,2),yCent(:,3),30,[1 1 0])
