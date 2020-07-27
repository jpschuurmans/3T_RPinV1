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
blobs = [s.Area].'; % checking where blobs excist adjecent areas with pix value 1
ind = find(blobs == blobs(1)); % index these pixels 
pix = s(ind).PixelList; % finding the "pixels" it belongs to
%creating the mask
MaskBack = logical(full(sparse(pix(:,2), pix(:,1), 1, size(blobFinding,1), size(blobFinding,2))));


signalcontrast = 0.45;
alpha = 1-signalcontrast;
SNR = signalcontrast/alpha;
%LC = [0.45 0.1]; % desired luminance and contrast

stimuli = {'Stim' 'MaskLSF' 'MaskHSF'}; %stimuli and mask

for theback = 1:length(imset.Back_scr) %for all scrambled backgrounds
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
                %the contrast, and sometimes luminance, seem to be off of
                %the facepix.. Why? no idea! So I'm normalizing again
                facepix = facepix - mean(facepix);
                facepix = facepix / std(facepix);
                facepix = (facepix*LC(2)) + LC(1);
                fprintf('mean: %f - std: %f - face %d for type: %s %s normalized\n',mean2(facepix),std2(facepix),theface,stimtype,stimulus) % check contr and lum for the background

                signalim(imset.faceindex_stimOnback{theface} ) = facepix; % replace face pixels of the original image by the equalized  ones
                %[mean2(signalim) std2(signalim)]
                signalim = signalim*signalcontrast;
                signalim =  (signalim.*(1-MaskAlpha) ) + (backim.* (MaskAlpha));			

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
                imshow(blendim); pause(0.15)
		
                imset.blendim{theback,thetype,thestim,theface} = blendim;     	

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
            imshow(backim); pause(0.15)
            imwrite(backim,[outfolder_back backname '.bmp'],'BMP')
        end
    end
end

save([basefolder outputmat],'-v7.3')


