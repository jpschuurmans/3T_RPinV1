%% alpha blending the stimuli in the white noise
% one way (as close as what xpman program does):  a weighted sum of the luminance values of each pixel of the image and the background. 
% I show how to do on a given image.
% this is what you should try and do while making the stimuli: determine which face goes on which
% frame when (and repeat this across conditions)

close all; clear all

basefolder = 'F:\JOLIEN\JOLIEN_STIMULI\';
load([basefolder 'JOLIEN_PROC.mat'])
addpath(genpath('C:\Users\vgoffaux\Documents\MATLAB\'))

load([basefolder 'JOLIEN_STIM02.mat'],'LC','*back', 'imset','nim','nblockspercondition','Background')

clear blend* Blend* alphaIm
stimweight = 0.5; % proportion of contrast is devoted to stimulus
alpha = 1-stimweight; % proportion of contrast is devoted to backrgound
SNR = stimweight/alpha;
% LC(2)/noiseC
% example:
theim = 10;
signalIm = imset.eq_stim{theim};
signalIm = signalIm*stimweight;
[mean2(signalIm) std2(signalIm)]

backIm = squeeze(Background.sequences{1}(:,:,1));
backIm = backIm*alpha;
[mean2(backIm) std2(backIm)]

alphaIm = (backIm + signalIm);
alphaIm = (alphaIm-mean2(alphaIm))/std2(alphaIm);
alphaIm_LC = [mean2(alphaIm) std2(alphaIm)] % image LC should be like initial LC
alphaIm = (alphaIm*0.08)+LC(1); % soften contrast
alphaIm_LC = [mean2(alphaIm) std2(alphaIm)] % image LC should be like initial LC
figure ('Color', [1 1 1]), imshow(alphaIm); title (['SNR = ' num2str(SNR)])
