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


xySize = size(imset.eq_stim{1});

finalSize = [550,550];
%finalSize = [500,500];
padSize = round((finalSize - xySize)/2);

[MaskIm,~,MaskAlpha] = (imread([basefolder 'blurrymask.png']));

MaskAlpha = single(MaskAlpha); MaskAlpha = imresize(MaskAlpha, finalSize);
MaskAlpha = MaskAlpha./max(MaskAlpha(:));
imshow(1-MaskAlpha)

%making average mask for normalization of noise
blobFinding = MaskAlpha;
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
%imshow(MaskBack)


signalcontrast = 0.5;
%LC = [0.45 0.1]; % desired luminance and contrast
%shiiBlend = cell(theim,length(nim));
%backy = cell(theim);
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
            if thestim == 1        
                if thetype == 1 %intact
                    set = imset.eq_stim;
                elseif thetype == 2 %negated
                    set = imset.neg_stim;
                elseif thetype == 3 %scrambled
                    set = imset.scr_stim;
                end
            else
                set = imset.mask(thetype,thestim-1,:);
            end
            for theface = 1:length(nim) %for all faces
                backim = imset.Back_scr{theback};
                temp = set{theface};
                temp =  (temp.*(1-MaskAlpha) ) + (backim.* (MaskAlpha));
                %imshow(temp)
       
                temp = temp-mean2(temp);
                temp = temp/std2(temp);
                temp = temp .* signalcontrast;
                temp = temp + LC(1); % [mean2(temp) std2(temp)] 
                backim = backim - mean2(backim); backim = backim/std2(backim); 
                backim = backim .* (1 - signalcontrast);
                backim = backim + LC(1); %[mean2(backim) std2(backim)]
                %imshow(backim)
                blendim = (temp + backim);%[mean2(backim) std2(backim)]
                blendim = blendim/std2(blendim); 
        
                %normalization to desired luminance and contrast
                corr = LC(2)/std2(blendim); blendim = blendim*corr;
                corr = LC(1)-mean2(blendim); blendim = blendim+corr;
                imshow(blendim)
                %[mean2(blendim) std2(blendim)]
                %backim = backy{thenois};
                %blendim(MaskBack) = backim(MaskBack);
                %imshow(blendim)
                
                imset.blendim{theback,thetype,thestim,theface} = blendim;
        
                if theface < 10
                    facenum = ['0' num2str(theface)];
                else
                    facenum = num2str(theface);
                end                
                
                stimtype = char(Cond1levels(thetype)); stimtype = stimtype(1:3);
                stimulus  = char(stimuli(thestim)) ;
                name = [backname '_' stimtype stimulus '_' facenum];
                
                imwrite(blendim,[outfolder_stim name],'BMP')
                
            end
            backim = imset.Back_scr{theback};
            imwrite(backim,[outfolder_back backname],'BMP')
        end
    end
    
    %imshow(backim)
end


% for times = 20:120
%     imshow(cell2mat(shiiBlend(2,times))); pause (0.5)
%     imshow(cell2mat(backy(2))); pause (0.5)
% end