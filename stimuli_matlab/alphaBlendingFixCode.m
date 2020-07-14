%% alpha blending the stimuli in the white noise
% one way (as close as what xpman program does):
% a weighted sum of the luminance values of each pixel of the image
% and the background. 
% I show how to do on a given image.
% this is what you should try and do while making the stimuli: 
% determine which face goes on which
% frame when (and repeat this across conditions)

close all; clear all
basefolder = '/home/jschuurmans/Documents/02_recurrentSF_3T/Stimuli/JOLIEN_STIM_MAIN/';
imagefolder = '/home/jschuurmans/Documents/02_recurrentSF_3T/Stimuli/JOLIEN_STIM_MAIN/stimuli/';
noisefolder = '/home/jschuurmans/Documents/02_recurrentSF_3T/Stimuli/JOLIEN_STIM_MAIN/noiseFrames/';
outfolder = '/home/jschuurmans/Documents/02_recurrentSF_3T/Stimuli/JOLIEN_STIM_MAIN/blendStim/';
load([basefolder 'JOLIEN_PROC.mat'])
basefolder = '/home/jschuurmans/Documents/02_recurrentSF_3T/Stimuli/JOLIEN_STIM_MAIN/';
load([basefolder 'JOLIEN_STIM02.mat'],'LC','*back', 'imset','nim','nblockspercondition','Background')

clear blend* Blend* alphaIm
stimweight = 0.5; % proportion of contrast is devoted to stimulus
alpha = 1-stimweight; % proportion of contrast is devoted to backrgound
SNR = stimweight/alpha;
% LC(2)/noiseC
% example:
theim = 10;
clear signalIm 
signalIm = imset.eq_stim{theim};
[mean2(signalIm) std2(signalIm)]
imshow(signalIm)
initMean = mean2(signalIm); %should be 0.4500
initSD = std2(signalIm); %should be 0.0350
signalIm = signalIm*stimweight;
[mean2(signalIm) std2(signalIm)]
imshow(signalIm)

clear backIm 
backIm = squeeze(Background.sequences{1}(:,:,1));
[mean2(backIm) std2(backIm)]
backIm = backIm*alpha;
[mean2(backIm) std2(backIm)]
imshow(backIm)

clear alphaIm
alphaIm = (backIm + signalIm);
alphaIm = (alphaIm-mean2(alphaIm))/std2(alphaIm);
alphaIm_LC = [mean2(alphaIm) std2(alphaIm)] % image LC should be like initial LC
alphaIm = (alphaIm*LC(2))+LC(1); % soften contrast
imshow(alphaIm)
alphaIm_LC = [mean2(alphaIm) std2(alphaIm)] % image LC should be like initial LC
figure ('Color', [1 1 1]), imshow(alphaIm); title (['SNR = ' num2str(SNR)])

%% fix backrgound issues
blobFinding = squeeze(imset.eq_stim{theim}); % need to use a mask to only select face pixels, give them the same LC as the face
blobFinding(imset.backindex_stimOnback{10}) = LC(1);
imshow(blobFinding) 

% making the background more distinct
blobFinding(blobFinding == blobFinding(1,1)) = 1;
% to create the mask, check where the value is 1
s = regionprops(blobFinding == 1 , 'Area', 'PixelList');
% checking where blobs excist
blobs = [s.Area].';
% to figure out where the blob is
ind = find(blobs == blobs(1));
% finding the "pixels" it belongs to
pix = s(ind).PixelList;

%creating the mask
MaskBack = logical(full(sparse(pix(:,2), pix(:,1), 1, size(blobFinding,1), size(blobFinding,2))));
%MaskIm = ~MaskBack;
imshow(MaskIm)


backIm = squeeze(Background.sequences{1}(:,:,1));
corr = std2(alphaIm(MaskBack))/std2(backIm);
backIm = backIm*corr;
corr = mean2(alphaIm(MaskBack))-mean2(backIm);
backIm = backIm+corr;


[mean2(alphaIm(MaskBack)) std2(alphaIm(MaskBack))]
[mean2(backIm) std2(backIm)]

for times = 1:10
    imshow(backIm); pause(0.5)
    imshow(alphaIm); pause(0.5)
end
%% fix backrgound issues
clear signalIm 
signalIm = squeeze(Background.sequences{1}(:,:,1)); % need to use a mask to only select face pixels, give them the same LC as the face
signalIm(imset.backindex_stimOnback{20}) = LC(1);
[mean2(signalIm) std2(signalIm)]
imshow(signalIm)
diff2 =  initSD/std2(signalIm); signalIm = signalIm*diff2;
diff = mean2(signalIm)-initMean; signalIm = signalIm - diff;
signalIm = signalIm*stimweight;
[mean2(signalIm) std2(signalIm)]
imshow(signalIm)


alphaIm2 = (backIm + signalIm);
alphaIm2 = (alphaIm2-mean2(alphaIm2))/std2(alphaIm2);
alphaIm2_LC = [mean2(alphaIm2) std2(alphaIm2)] % image LC should be like initial LC
alphaIm2 = (alphaIm2*LC(2))+LC(1); % soften contrast
imshow(alphaIm2)
alphaIm2_LC = [mean2(alphaIm2) std2(alphaIm2)] % image LC should be like initial LC
figure ('Color', [1 1 1]), imshow(alphaIm2); title (['SNR = ' num2str(SNR)])

for times = 1:10
    imshow(alphaIm2); pause(0.5)
    imshow(alphaIm); pause(0.5)
end
