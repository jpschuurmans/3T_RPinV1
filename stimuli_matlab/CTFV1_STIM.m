close all; clear; clc

basefolder = '/home/jschuurmans/Documents/02_recurrentSF_3T/recurrentSF_3T_CodeRepo/stimuli_matlab/';
disp(['basefolder: ', basefolder])
load([basefolder 'CTFV1_PROC.mat'])

addpath(genpath([basefolder  'AmpPlotExp']))
addpath(basefolder)
%addpath(genpath('C:\Users\vgoffaux\Documents\MATLAB\'))

LC = [0.45 0.1]; % desired luminance and contrast
imagefolder = [basefolder '01greenback/'] ;
nim = dir([imagefolder '*.bmp']);

%POSorNEG = 1; % 1=positive; 2=negative contrast

outputmat = 'CTFV1_STIM.mat';

%% prepare face images
% load the images, detect face versus background pixels, set luminance and contrast of face pixels
% to 0 and 1, repectively

scalefactor = [4 2]; % scales used to shrink face images used as stimuli and background image
for theim = 1:length(nim)
    im_stim = double(imread([imagefolder nim(theim).name]))/256; % read
    im_stim = imresize(im_stim,1/scalefactor(2),'nearest'); % downscale
    imset.raw_back{theim} = im_stim; % original sized images are kept for the generation of the scrambled background
    im_stim = imresize(im_stim,1/(scalefactor(1)/scalefactor(2)),'nearest'); % downscale
    imset.raw_stim{theim} = im_stim;
end
xySize_raw = size(im_stim);
xySize_stim = [max(xySize_raw) max(xySize_raw)];
xySize_back = xySize_stim* (scalefactor(1)/scalefactor(2));
paddims_stim = max(xySize_raw(:,1:2)) - min(xySize_raw(:,1:2)); % make a square image

%% Load images, measure L and C, index face/back pixels for stimulus
for theim = 1:length(nim)
    clear im_stim
    im_stim = imset.raw_stim{theim} ;
    im_stim = padarray(im_stim,[0 round(paddims_stim/2)],'replicate'); % if images are not square.
    im_stim = im_stim(1:max(xySize_stim),1:max(xySize_stim),:);
    
    sizeprod = 1: (size(im_stim,1)*size(im_stim,2));
    back = cell(1,3);
    for thechannel = 1:3 % find background pixels based on the weird color given to them in e.g. Photoshop, channel by channel
        back{thechannel} = find(im_stim(:,:,thechannel) == im_stim(1,1,thechannel));
    end
    step1 =  intersect(back{1},back{2});
    imset.backindex_stim{theim} = intersect(step1,back{3});
    imset.faceindex_stim{theim} = setdiff(sizeprod',imset.backindex_stim{theim}); % find face pixels
%     length(imset.backindex_stim{theim}) + length(imset.faceindex_stim{theim})
    im_stim = rgb2gray(im_stim); % convert to gray scales
    imset.gray_stim{theim} = im_stim;
end
im2avg_stim = zeros(length(nim),xySize_back(1),xySize_back(2));
paddims_back = xySize_back(1) - xySize_stim(1); % make a square image of same dimensions as background


for theim = 1:length(nim)
    im_stimb = imset.gray_stim{theim};
    facepix = im_stimb(imset.faceindex_stim{theim}); % select face pixels
    facepix  = imadjust(facepix,[0; 1],[.1; .9]);%change the range to avoid clipping further down
    facepix = facepix - mean(facepix); % normalize face pixel values (step1)
    facepix = facepix/std(facepix); % normalize face pixel values (step2)
    fprintf('%d norm check - mean: %d - std: %d\n',theim,mean(facepix),std(facepix))
    im_stimb(imset.faceindex_stim{theim}) = facepix; % replace face pixels of the original image by the normalized ones
%     backpix = im_stimb(imset.backindex_stim{theim});%set backpixels to 0.5 for negation
%     diff = 0.5/mean(backpix);
%     backpix = backpix*diff;
%     im_stimb(imset.backindex_stim{theim}) = backpix; % replace bacl pixels of the original image by the 0.5 ones
    imset.norm_stim{theim}  = im_stimb;
    
    facepix = (facepix*LC(2)) + LC(1);
    fprintf('%d norm check - mean: %d - std: %d\n',theim,mean(facepix),std(facepix))
    im_stimb(imset.faceindex_stim{theim} ) = facepix; % replace face pixels of the original image by the equalized  ones
    
    im_stimb = padarray(im_stimb,[round(paddims_back/2) round(paddims_back/2)],'replicate'); % pad to get the same dimensions as background image.
    im_stimb = im_stimb(1:xySize_back(1),1:(xySize_back));
    imset.eq_stim{theim}  = im_stimb; 
   
    
    im2avg_stim(theim,:,:) = im_stimb;
    imshow(imset.eq_stim{theim}); pause(0.15)
    
    imset.neg_stim{theim}  = 1 - im_stimb; 
   
    imshow(imset.neg_stim{theim}); pause(0.15)
    clear facepix
    facepix = imset.neg_stim{theim}(imset.faceindex_stim{theim}); % select face pixels 
    fprintf('%d norm check - mean: %d - std: %d\n',theim,mean(facepix),std(facepix))

end


avgface = squeeze(mean(im2avg_stim,1)); imshow(avgface)
imwrite(avgface,[basefolder 'avgface_set' num2str(theim) '.bmp'],'BMP');

% for presentation of faces on background: find the central face pixels on COLOR 1100*1100 background images (the latter are generated in code STIM02)
for theim = 1:length(nim)
    clear im_stim
    im_stim = imset.raw_stim{theim} ;
    im_stim = padarray(im_stim,[0 round(paddims_stim/2)],'replicate'); % if images are not square.
    im_stim = im_stim(1:max(xySize_stim),1:max(xySize_stim),:);% % % % % % % % %
    im_stim = padarray(im_stim,[round(paddims_back/2) round(paddims_back/2)],'replicate'); % if images are not square.
    im_stim =  im_stim(1:xySize_back(1),1:(xySize_back),:); 
    clear sizeprod
    sizeprod = 1: (size(im_stim,1)*size(im_stim,2));
    for thechannel = 1:3 % find background pixels based on the weird color given to them in e.g. Photoshop, channel by channel
        back{thechannel} = find(im_stim(:,:,thechannel) == im_stim(1,1,thechannel));
    end
    step1 =  intersect(back{1},back{2});
    imset.backindex_stimOnback{theim} = intersect(step1,back{3});
    imset.faceindex_stimOnback{theim} = setdiff(sizeprod',imset.backindex_stim{theim}); % find face pixels
end

%% make sure that the uniform background of stimulus images is = to LC(1) (isoluminant)

for theim = 1:length(nim)
    imset.eq_stim{theim}(imset.backindex_stimOnback{theim})  = LC(1); %%%%%%%%%%%%%%%%%%%% Images to use as intact stimuli
    imshow(imset.eq_stim{theim})
    imset.neg_stim{theim}(imset.backindex_stimOnback{theim})  = LC(1); %%%%%%%%%%%%%%%%%%%% Images to use as negated stimuli
    imshow(imset.neg_stim{theim})
end

%% iterative scrambling: we do that so that scrambled stimuli generated later are not too contaminated by the uniform background
fig_over_back_ratio = length(facepix)/prod(xySize_stim); % proportion of face versus background pixels of one example face 
niter = 500; % should be several hundreds [should simulate how many iterations are necessary foramplot of intact and scrambled face area to match]
clear iterscrface
for theim = 1:length(nim)
    scrimage = phaseScrambleImage(imset.norm_stim{theim});
    combiface = scrimage;
    combiface( imset.faceindex_stim{theim}) =  imset.norm_stim{theim}(imset.faceindex_stim{theim}) ;
    combiface(imset.backindex_stim{theim}) =  scrimage(imset.backindex_stim{theim}) ;
    combiface = (combiface-mean2(combiface))/std2(combiface);
    fprintf('%d iterative scrambling - mean: %d - std: %d\n',theim,mean(mean2(combiface)),std2(combiface))
    clear scrimage
    iterscrface_stim = cell(1,niter); %preallocation
    for theiter = 1:niter
        
        if theiter == 1
            interim = combiface;
        elseif theiter > 1
            interim = iterscrface_stim{theiter-1};
        end
        
        scrimage = phaseScrambleImage(interim);
        scrimage(imset.faceindex_stim{theim}) = imset.norm_stim{theim}(imset.faceindex_stim{theim}) ;
        scrimage = (scrimage-mean2(scrimage))/std2(scrimage);
        iterscrface_stim{theiter} = scrimage;
%         imshow(iterscrface_stim{theiter},[]);
    end
    imset.iter_stim{theim} = iterscrface_stim{theiter};
%     imshow(imset.iter_stim{theim},[]);
end


%% amplitude spectrum 
ntypes=length(stimtype);
SFres = 20; % resolution of SF sampling (n SF bins) 
% the range we will work with going from 1 c/image to m*sqrt(2) c/image, m being size(im,1)
clear SFspec
for theim = 1:length(nim)
    clear AmpHist*
    im_stim = imset.iter_stim{theim};
    im_stim = (im_stim/std2(im_stim)) - mean2(im_stim);
    AmpPlot_VG2(im_stim,SFres,1);% AmpPlot(im,<NoScaleBins>,<NoOrientBins>,<graphics>)
    load([basefolder 'amplot.mat'])
    %load('C:\Users\vgoffaux\Documents\MATLAB\amplot');
    %     imset.SFslope{theim} = p(1);
    SFspec.SFhist(theim,:) = AmpHist;
    SFspec.SFslope{theim} = p;
    SFspec.linSF{theim} = PredAmp;                                       % And the predicted amplitude based on fitted line
%     subplot(round(length(nim)/5),round(length(nim)/round(length(nim)/5)),theim)
%     loglog(exp(fineScale),PredAmp,'k-')
%     loglog(Scales,sum(AmpHist,2)','ko',exp(fineScale),PredAmp,'b-')
%      legend(sprintf('Slope of amplitude spectrum is %3.3f ',p(1)));
end

allsfslope = vertcat(SFspec.SFslope{:});
SFspec.SFslope_ga = {mean(allsfslope,1) std(allsfslope,1)};
SFspec.SFhist_ga = {mean(SFspec.SFhist,1) std(SFspec.SFhist,1)};


close all; 
set(0,'defaultlinelinewidth',3)
lineIM = cool(length(nim));
figure('Position', [100, 100, 1000, 1000],'Color',[1 1 1]);
plot(log(Scales),log(SFspec.SFhist_ga{1}));
title('Amplitude as a function of SF (log)'); xlabel('log SF (c/image)');ylabel('Amplitude');

loglog(Scales,sum(AmpHist,2)','bd',exp(fineScale),PredAmp,'b-')

%[...] compute AUC and define LSF and HSF cutoff that energy is similar 



%% scramble phase
nscrversions_perFace= 4; %the same mask across normal, negated, and scrambled conditions (n = 1), also need a scrambled stimulus (n=2) , and 2 versions (because 2 block repetitions per run)
maskcontrast = LC(2)*2.5; % mask had higher contrast for masking efficiency
clear amplim phasim i
amplim = cell(1,length(nim)); %prealocate
phasim = cell(1,length(nim)); %prealocate
% filter intact and scrambled images
opt = struct;
opt.type = 'butt';
opt.order = 2;
opt.whichfilter = 2;
LSFcutoff = [1 8.5]; % lsf cutoff 3 octaves
HSFcutoff = [8.5 (xySize_stim(1)/2)]; %4 octaves -- making 2 ranges adjecent
% sf octaves!!

for theim=1:length(nim)
    clear daimage im_stim
    daimage=imset.iter_stim{theim};
    fftimage=fftshift(fft2(daimage,xySize_stim(1), xySize_stim(2)));
    amplim{theim}=abs(fftimage);
    phasim{theim}=angle(fftimage);
    
    for thescr = 1:nscrversions_perFace
        if thescr == 1 %for the scrambed condition
            clear angleV facepix
            angleV= reshape((phasim{theim}), 1, numel(phasim{theim}));
            angle_scr= angleV(randperm(length(angleV)));
            rphasim = reshape(angle_scr, size(daimage));
            randspect = amplim{theim}.*exp(1i*rphasim);
            realrandspect = real(ifft2(fftshift(randspect))); %inverse FFT: note that you only keep the real and not the imagenary part of the complex nrs
            facepix = realrandspect(imset.faceindex_stim{theim});
            facepix = facepix - mean(facepix); % normalize face pixel values (step1)
            facepix = facepix/std(facepix); % normalize face pixel values (step2)
            facepix = (facepix*LC(2)) + LC(1);
            fprintf('%d norm check scr - mean: %d - std: %d\n',theim,mean(facepix),std(facepix)) % check normalization worked
            realrandspect(imset.faceindex_stim{theim} ) = facepix; % replace face pixels of the original image by the normalized ones
            realrandspect(imset.backindex_stim{theim} ) = LC(1); % isoluminant background
        
            im_stim = padarray(realrandspect,[round(paddims_back/2) round(paddims_back/2)],'replicate'); % pad to get the same dimensions as background image.
            im_stim =  im_stim(1:xySize_back(1),1:(xySize_back),:); 

            imset.scr_stim{theim} = im_stim; %%%%%%%%%%%%%%%%%%%% Images to use as scrambled stimuli
            imshow(imset.scr_stim{theim}); pause (0.1)
        else %mask conditions for stim intact/negated/scrambled
            for thesf = 1:length(Cond3levels) %for nr of SFs
                clear temp facepix
                if thesf == 1 % first for LSF
                    opt.cutoff = LSFcutoff; % LSF faces
                elseif thesf == 2 %then for HSF
                    opt.cutoff = HSFcutoff; % HSF faces
                end
                clear angleV facepix
                angleV= reshape((phasim{theim}), 1, numel(phasim{theim}));
                angle_scr= angleV(randperm(length(angleV)));
                rphasim = reshape(angle_scr, size(daimage));
                randspect = amplim{theim}.*exp(1i*rphasim);
                realrandspect = real(ifft2(fftshift(randspect))); %inverse FFT: note that you only keep the real and not the imagenary part of the complex nrs
                temp = KP_SF_Filter(realrandspect,opt); %actually filtering it 
                facepix = temp(imset.faceindex_stim{theim});
            
                facepix = facepix - mean(facepix); % normalize face pixel values (step1)
                facepix = facepix/std(facepix); % normalize face pixel values (step2)
                facepix = (facepix*maskcontrast) + LC(1);
                fprintf('%d norm check mask - mean: %d - std: %d\n',theim,mean(facepix),std(facepix)) % check normalization worked
                realrandspect(imset.faceindex_stim{theim} ) = facepix; % replace face pixels of the original image by the normalized ones
                realrandspect(imset.backindex_stim{theim} ) = LC(1); % isoluminant background
        
                im_stim = padarray(realrandspect,[round(paddims_back/2) round(paddims_back/2)],'replicate'); % pad to get the same dimensions as background image.
                im_stim =  im_stim(1:xySize_back(1),1:(xySize_back),:); 
                thetype = thescr-1;
                imset.mask{thetype,thesf,theim} = im_stim;%%%%%%%%%%%%%%%%%%%% Images to use as mask stimuli
                imshow(imset.mask{thetype,thesf,theim}); pause (0.1)
            end
        end
      
    end
end


fig = figure('Color',[LC(1) LC(1) LC(1)]);
count = 0;
for thesf = 1:length(Cond3levels) %for both SFs
    for thetype = 1:length(stimtype) %for all conditions
        count = count  + 1;
        subplot(length(Cond3levels),length(stimtype),count)
        imshow(imset.mask{thetype,thesf,1})

    end
end

disp('saving..')
save([basefolder outputmat],'-v7.3')


%% saving the images

%%%%%%%%%%%%%%%%%%% use next code to create the background
%%%%%%%%%%%%%%%%%%% then apply alphablending
%%%%%%%%%%%%%%%%%%% after this save all the images!


% theim = 1; % 1 tm 24
% thetype = 1; % 1 tm 3 (int/neg/scr)
% thesf = 1; % 1 or 2 (LSF/HSF)
% %stim
% imshow(imset.eq_stim{theim})%intact faces
% imshow(imset.neg_stim{theim}) %negated faces
% imshow(imset.scr_stim{theim}) %phase scrambled faces
% %masks
% imshow(imset.mask{thetype,thesf,theim}) %for 3 conditions -> HSF+LSF

