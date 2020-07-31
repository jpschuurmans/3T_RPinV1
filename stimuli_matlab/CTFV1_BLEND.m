%% alpha blending the stimuli in the white noise
% one way (as close as what xpman program does):
% a weighted sum of the luminance values of each pixel of the image
% and the background. 

close all; clear; clc

basefolder = '/home/jschuurmans/Documents/02_recurrentSF_3T/recurrentSF_3T_CodeRepo/stimuli_matlab/';
outfolder_stim = [basefolder 'stimuli/'];
outfolder_back = [basefolder 'background/'];
load([basefolder 'CTFV1_PROC.mat'])
addpath(basefolder)

load([basefolder 'CTFV1_BACK.mat'],'LC','*back', 'imset','nim','nblockspercondition')

%inact faces:       imshow(imset.eq_stim{2})
%negated faces:     imshow(imset.neg_stim{1})
%scrambled faces:   imshow(imset.scr_stim{1})
%masks:             imset.mask{thetype,thesf,theim}
%background:        imset.Back_scr{theframe}

outputmat = 'CTFV1_BLEND.mat';

xySize = size(imset.eq_stim{1});
finalSize = [550,550];
padSize = round((finalSize - xySize)/2);

[MaskIm,~,MaskAlpha] = (imread([basefolder 'blurrymask.png']));

MaskAlpha = single(MaskAlpha); MaskAlpha = imresize(MaskAlpha, finalSize);
MaskAlpha = MaskAlpha./max(MaskAlpha(:));
imshow(1-MaskAlpha)

%%%%%%%%%%%%%% is necessary for selecting backgroundpixels since
%%%%%%%%%%%%%% the blurrymask contains pixels in the border of
%%%%%%%%%%%%%% the outline with the same value as the background 
%making average mask for normalization of noise
blobFinding = MaskAlpha;
blobFinding(blobFinding == blobFinding(1,1)) = 1; % making the background more distinct
s = regionprops(blobFinding == 1 , 'Area', 'PixelList'); % to create the mask, check where the value is 1
t = regionprops(blobFinding == 0 , 'Area', 'PixelList');
blobs = [s.Area].'; % checking where blobs excist adjecent areas with pix value 1
blobsFace = [t.Area].';
ind = find(blobs == blobs(1)); % index these pixels 
indFace = find(blobsFace == blobsFace(1));
pix = s(ind).PixelList; % finding the "pixels" it belongs to
pixFace = t(indFace).PixelList; 
%creating the mask
MaskBack = logical(full(sparse(pix(:,2), pix(:,1), 1, size(blobFinding,1), size(blobFinding,2))));
MaskFace = logical(full(sparse(pixFace(:,2), pixFace(:,1), 1, size(blobFinding,1), size(blobFinding,2))));
%imshow(MaskBack)
%imshow(MaskFace)

signalcontrast = 0.45;
alpha = 1-signalcontrast;
SNR = signalcontrast/alpha;
%LC = [0.45 0.1]; % desired luminance and contrast

stimuli = {'Stim' 'MaskLSF' 'MaskHSF'}; %stimuli and mask

%preallocate for speed
finalstim_backpixLC = cell(length(imset.Back_scr),length(Cond1levels),length(stimuli)); %preallocate
finalstim_facepixLC = cell(length(imset.Back_scr),length(Cond1levels),length(stimuli)); %preallocate
finalbackim_backpixLC = cell(length(imset.Back_scr),length(Cond1levels),length(stimuli)); %preallocate
finalbackim_facepixLC = cell(length(imset.Back_scr),length(Cond1levels),length(stimuli)); %preallocate

for theback = 1:10 %length(imset.Back_scr) %for all scrambled backgrounds
    fprintf('bleding and safing images for %d background \n',theback)
    if theback < 10
        backname = ['bg0' num2str(theback)];
    else
        backname = ['bg' num2str(theback)];
    end
    for thetype = 1:length(Cond1levels) % intact, negated and scrambled
        for thestim = 1:length(stimuli) %stim, maskLSF, maskHSF
            %naming for checking and saving
            stimtype = char(Cond1levels(thetype)); stimtype = stimtype(1:3);
            stimulus  = char(stimuli(thestim)) ;
            if thestim == 1        
                if thetype == 1 %intact
                    set = imset.eq_stim;
                elseif thetype == 2 %negated
                    set = imset.neg_stim;
                elseif thetype == 3 %scrambled 
                    set = imset.scr_stim;
                end
            elseif thestim == 2 %Mask LSF
                set = imset.mask(thetype,thestim-1,:);
            elseif thestim == 3 %Mask HSF 
                set = imset.mask(thetype,thestim-1,:);
            end
            for theface = 1:length(nim) %for all faces
                backim = imset.Back_scr{theback};
                %imshow(backim)
                fprintf('mean: %f - std: %f - back %d\n',mean2(backim),std2(backim),theback) % check contr and lum for the background
                backim = backim*alpha;

                signalim = set{theface};
                %imshow(signalim)
                facepix = signalim(imset.faceindex_stimOnback{theface});
                fprintf('mean: %f - std: %f - face %d for type: %s %s\n',mean2(facepix),std2(facepix),theface,stimtype,stimulus) % check contr and lum for the background

                signalim = signalim*signalcontrast;
                signalim =  (signalim.*(1-MaskAlpha) ) + (backim.* (MaskAlpha));			

                %imshow(signalim)
                if thestim == 1 % stimulus that needs blending with background
                    blendim = (signalim + backim);
                else % a mask that doesnt need blending
                    blendim = signalim;
                end
                
                %imshow(blendim)
                blendim = blendim - mean2(blendim); %normalize blend stim part 1
                blendim = blendim / std2(blendim); %normalize blend stim part 2
                blendim	= (blendim*LC(2)) + LC(1); %desired lum and contrast
                fprintf('mean: %f - std: %f - face %d for type: %s %s blendedddd\n',mean2(blendim),std2(blendim),theface,stimtype,stimulus) % check contr and lum for the background
                
                % replace background pixels of the blend image by the original ones
                backim = imset.Back_scr{theback};
                blendim(MaskBack) = backim(MaskBack);
                imshow(blendim); 
		
                imset.blendim{theback,thetype,thestim,theface} = blendim;     	
                
                finalstim_backpixLC{theback,thetype,thestim}(theface,:) = [mean(blendim(imset.backindex_stimOnback{theface})) std(blendim(imset.backindex_stimOnback{theface}))]; %%%% $$$$$$
                finalstim_facepixLC{theback,thetype,thestim}(theface,:) = [mean(blendim(imset.faceindex_stimOnback{theface})) std(blendim(imset.faceindex_stimOnback{theface}))]; %%%% $$$$$$
                
                % saving the stimuli with correct naming
                if theface < 10
                    facenum = ['0' num2str(theface)];
                else
                    facenum = num2str(theface);
                end                
                
                stimtype = char(Cond1levels(thetype)); stimtype = stimtype(1:3);
                stimulus  = char(stimuli(thestim)) ;
                name = [backname '_' stimtype stimulus '_' facenum];
                
                imwrite(blendim,[outfolder_stim name '.bmp'],'BMP')
                
            end
            backim = imset.Back_scr{theback};
            imshow(backim); 
            finalbackim_backpixLC{theback,thetype,thestim} = [mean(backim(MaskBack)) std(backim(MaskBack))]; %%%% $$$$$$
            finalbackim_facepixLC{theback,thetype,thestim} = [mean(backim(MaskFace)) std(backim(MaskFace))] ;%%%% $$$$$$
         
            imwrite(backim,[outfolder_back backname '.bmp'],'BMP')
        end
    end
end

%% CHECK plot luminance and contrast
% check stimuli first
clear dataStimLback dataStimCback dataStimLface dataStimCface
clear vecdataStimLback vecdataStimLface vecdataStimCback vecdataStimCface

%preallocating
dataStimLback = zeros(10,length(finalstim_backpixLC(:,1))); dataStimCback = dataStimLback; dataStimLface = dataStimLback; dataStimCface = dataStimLback;
vecdataStimLback = zeros(length(Cond1levels),length(reshape(dataStimCface,numel(dataStimCface),1))); vecdataStimLface = vecdataStimLback; vecdataStimCback = vecdataStimLback; vecdataStimCface = vecdataStimLback;


thestim = 1; %stim, maskLSF, maskHSF
for thetype = 1:length(Cond1levels) % intact, negated and scrambled
    for theback = 1:10 %for all scrambled backgrounds
        dataStimLback(theback,:) = finalstim_backpixLC{theback,thetype,thestim}(:,1);
        dataStimCback(theback,:) = finalstim_backpixLC{theback,thetype,thestim}(:,2);
        dataStimLface(theback,:) = finalstim_facepixLC{theback,thetype,thestim}(:,1);
        dataStimCface(theback,:) = finalstim_facepixLC{theback,thetype,thestim}(:,2);
    end
    
    vecdataStimLback(thetype,:) = reshape(dataStimLback,numel(dataStimLback),1);
    vecdataStimLface(thetype,:) = reshape(dataStimLface,numel(dataStimLface),1);
    vecdataStimCback(thetype,:) = reshape(dataStimCback,numel(dataStimCback),1);
    vecdataStimCface(thetype,:) = reshape(dataStimCface,numel(dataStimCface),1);
end


close all
colorsc = hsv(length(Cond1levels));
figure
subplot(2,2,1)
for thetype = 1:length(Cond1levels) % intact, negated and scrambled
    plot(vecdataStimLback(thetype,:)','-o','Color',colorsc(thetype,:))
    hold on
end
title('Luminance of back pixels across images and blocks')
legend('Intact','Negated','Scrambled')
ylim ([0.35 0.55])
text(4,0.51,'intact')
text(100,0.51,['mean: ' num2str(mean(vecdataStimLback(1,:))) ', std: ' num2str(std(vecdataStimLback(1,:)))])
text(4,0.50,'negated')
text(100,0.50,['mean: ' num2str(mean(vecdataStimLback(2,:))) ', std: ' num2str(std(vecdataStimLback(2,:)))])
text(4,0.49,'scrambled')
text(100,0.49,['mean: ' num2str(mean(vecdataStimLback(3,:))) ', std: ' num2str(std(vecdataStimLback(3,:)))])



subplot(2,2,2)
for thetype = 1:length(Cond1levels) % intact, negated and scrambled
    plot(vecdataStimLface(thetype,:)','-o','Color',colorsc(thetype,:))
    hold on
end
ylim ([0.35 0.55])
title('Luminance of face pixels across images and blocks')
legend('Intact','Negated','Scrambled')
text(4,0.51,'intact')
text(100,0.51,['mean: ' num2str(mean(vecdataStimLface(1,:))) ', std: ' num2str(std(vecdataStimLface(1,:)))])
text(4,0.50,'negated')
text(100,0.50,['mean: ' num2str(mean(vecdataStimLface(2,:))) ', std: ' num2str(std(vecdataStimLface(2,:)))])
text(4,0.49,'scrambled')
text(100,0.49,['mean: ' num2str(mean(vecdataStimLface(3,:))) ', std: ' num2str(std(vecdataStimLface(3,:)))])


subplot(2,2,3)
for thetype = 1:length(Cond1levels) % intact, negated and scrambled
    plot(vecdataStimCback(thetype,:)','-o','Color',colorsc(thetype,:))
    hold on
end
ylim ([0.05 0.15])
title('Contrast of back pixels across images and blocks')
legend('Intact','Negated','Scrambled')
text(4,0.125,'intact')
text(100,0.125,['mean: ' num2str(mean(vecdataStimCback(1,:))) ', std: ' num2str(std(vecdataStimCback(1,:)))])
text(4,0.12,'negated')
text(100,0.12,['mean: ' num2str(mean(vecdataStimCback(2,:))) ', std: ' num2str(std(vecdataStimCback(2,:)))])
text(4,0.115,'scrambled')
text(100,0.115,['mean: ' num2str(mean(vecdataStimCback(3,:))) ', std: ' num2str(std(vecdataStimCback(3,:)))])


subplot(2,2,4)
for thetype = 1:length(Cond1levels) % intact, negated and scrambled
    plot(vecdataStimCface(thetype,:)','-o','Color',colorsc(thetype,:))
    hold on
end
ylim ([0.05 0.15])
title('Contrast of face pixels across images and blocks')
legend('Intact','Negated','Scrambled')
text(4,0.125,'intact')
text(100,0.125,['mean: ' num2str(mean(vecdataStimCface(1,:))) ', std: ' num2str(std(vecdataStimCface(1,:)))])
text(4,0.120,'negated')
text(100,0.120,['mean: ' num2str(mean(vecdataStimCface(2,:))) ', std: ' num2str(std(vecdataStimCface(2,:)))])
text(4,0.115,'scrambled')
text(100,0.115,['mean: ' num2str(mean(vecdataStimCface(3,:))) ', std: ' num2str(std(vecdataStimCface(3,:)))])





%% do the same for background stimuli
clear dataBackLback dataBackCback dataBackLface dataBackCface
clear vecdataBackLback vecdataBackLface vecdataBackCback

%preallocate
dataBackLback = zeros(10,length(finalbackim_backpixLC(:,1)));dataBackCback = dataBackLback; dataBackLface = dataBackLback; dataBackCface = dataBackLback;
vecdataBackLback = zeros(length(Cond1levels), length(reshape(dataBackLback,numel(dataBackLback),1))); vecdataBackLface = vecdataBackLback; vecdataBackCback = vecdataBackLback; vecdataBackCface = vecdataBackLback;

thestim = 1; %stim, maskLSF, maskHSF
for thetype = 1:length(Cond1levels) % intact, negated and scrambled
    for theback = 1:10 %for all scrambled backgrounds
        dataBackLback(theback,:) = finalbackim_backpixLC{theback,thetype,thestim}(:,1);
        dataBackCback(theback,:) = finalbackim_backpixLC{theback,thetype,thestim}(:,2);
        dataBackLface(theback,:) = finalbackim_facepixLC{theback,thetype,thestim}(:,1);
        dataBackCface(theback,:) = finalbackim_facepixLC{theback,thetype,thestim}(:,2);
    end
    vecdataBackLback(thetype,:) = reshape(dataBackLback,numel(dataBackLback),1);
    vecdataBackLface(thetype,:) = reshape(dataBackLface,numel(dataBackLface),1);
    vecdataBackCback(thetype,:) = reshape(dataBackCback,numel(dataBackCback),1);
    vecdataBackCface(thetype,:) = reshape(dataBackCface,numel(dataBackCface),1);
end

figure
subplot(2,2,1)
for thetype = 1:length(Cond1levels) % intact, negated and scrambled
    plot(vecdataBackLback(thetype,:)','-o','Color',colorsc(thetype,:))
    hold on
end
title('Luminance of back pixels across background images and blocks')
legend('Intact','Negated','Scrambled')
ylim ([0.35 0.55])
text(4,0.51,'intact')
text(100,0.51,['mean: ' num2str(mean(vecdataBackLback(1,:))) ', std: ' num2str(std(vecdataStimLback(1,:)))])
text(4,0.50,'negated')
text(100,0.50,['mean: ' num2str(mean(vecdataBackLback(2,:))) ', std: ' num2str(std(vecdataStimLback(2,:)))])
text(4,0.49,'scrambled')
text(100,0.49,['mean: ' num2str(mean(vecdataBackLback(3,:))) ', std: ' num2str(std(vecdataStimLback(3,:)))])



subplot(2,2,2)
for thetype = 1:length(Cond1levels) % intact, negated and scrambled
    plot(vecdataBackLface(thetype,:)','-o','Color',colorsc(thetype,:))
    hold on
end
ylim ([0.35 0.55])
title('Luminance of face pixels across background images and blocks')
legend('Intact','Negated','Scrambled')
text(4,0.51,'intact')
text(100,0.51,['mean: ' num2str(mean(vecdataBackLface(1,:))) ', std: ' num2str(std(vecdataStimLface(1,:)))])
text(4,0.50,'negated')
text(100,0.50,['mean: ' num2str(mean(vecdataBackLface(2,:))) ', std: ' num2str(std(vecdataStimLface(2,:)))])
text(4,0.49,'scrambled')
text(100,0.49,['mean: ' num2str(mean(vecdataBackLface(3,:))) ', std: ' num2str(std(vecdataStimLface(3,:)))])


subplot(2,2,3)
for thetype = 1:length(Cond1levels) % intact, negated and scrambled
    plot(vecdataBackCback(thetype,:)','-o','Color',colorsc(thetype,:))
    hold on
end
ylim ([0.05 0.15])
title('Contrast of back pixels across background images and blocks')
legend('Intact','Negated','Scrambled')
text(4,0.125,'intact')
text(100,0.125,['mean: ' num2str(mean(vecdataBackCback(1,:))) ', std: ' num2str(std(vecdataStimCback(1,:)))])
text(4,0.12,'negated')
text(100,0.12,['mean: ' num2str(mean(vecdataBackCback(2,:))) ', std: ' num2str(std(vecdataStimCback(2,:)))])
text(4,0.115,'scrambled')
text(100,0.115,['mean: ' num2str(mean(vecdataBackCback(3,:))) ', std: ' num2str(std(vecdataStimCback(3,:)))])


subplot(2,2,4)
for thetype = 1:length(Cond1levels) % intact, negated and scrambled
    plot(vecdataBackCface(thetype,:)','-o','Color',colorsc(thetype,:))
    hold on
end
ylim ([0.05 0.15])
title('Contrast of face pixels across background images and blocks')
legend('Intact','Negated','Scrambled')
text(4,0.125,'intact')
text(100,0.125,['mean: ' num2str(mean(vecdataBackCface(1,:))) ', std: ' num2str(std(vecdataStimCface(1,:)))])
text(4,0.120,'negated')
text(100,0.120,['mean: ' num2str(mean(vecdataBackCface(2,:))) ', std: ' num2str(std(vecdataStimCface(2,:)))])
text(4,0.115,'scrambled')
text(100,0.115,['mean: ' num2str(mean(vecdataBackCface(3,:))) ', std: ' num2str(std(vecdataStimCface(3,:)))])


%%






save([basefolder outputmat],'-v7.3')


