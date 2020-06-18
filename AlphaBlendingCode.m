close all; clear all; clc

%create paths to folders
basefolder = '/home/jschuurmans/Documents/02_recurrentSF_3T/Stimuli/JOLIEN_STIM_MAIN/';
imagefolder = '/home/jschuurmans/Documents/02_recurrentSF_3T/Stimuli/JOLIEN_STIM_MAIN/stimuli/';
noisefolder = '/home/jschuurmans/Documents/02_recurrentSF_3T/Stimuli/JOLIEN_STIM_MAIN/noiseFrames/';
outfolder = '/home/jschuurmans/Documents/02_recurrentSF_3T/Stimuli/JOLIEN_STIM_MAIN/blendStim/';
nim = dir([imagefolder '*.bmp']);
noi = dir([noisefolder '*.bmp']);

%load the stimuli + noise frames
for theim = 1:length(nim)
	im_stim = double(imread([imagefolder nim(theim).name]))/256; % read
    imset.raw_face{theim} = im_stim;
end
for theim = 1:length(noi)
	im_stim = double(imread([noisefolder noi(theim).name]))/256; % read
    imset.raw_noise{theim} = im_stim;
end

xySize = size(im_stim);

finalSize = size(imset.raw_face{theim});
%finalSize = [500,500];
padSize = round((finalSize - xySize)/2);

[MaskIm,~,MaskAlpha] = (imread([basefolder 'blurrymask.png']));

MaskAlpha = single(MaskAlpha); MaskAlpha = imresize(MaskAlpha, finalSize);
MaskAlpha = MaskAlpha./max(MaskAlpha(:));
imshow(1-MaskAlpha)

%making mask for normalization of noise
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
LC = [0.45 0.1]; % desired luminance and contrast
shiiBlend = cell(theim,length(nim));
backy = cell(theim);
for thenois =1:theim %for all noises
    backim = imset.raw_noise{thenois};
    corr = LC(2)/std2(backim); backim = backim*corr;
    corr = LC(1)-mean2(backim); backim = backim+corr;
    backy{thenois} = backim;
    for theface = 1:length(nim) %for all stimuli (faces)
        temp = padarray(imset.raw_face{theface},padSize,'replicate');
        backim = backy{thenois};
        %imshow(backim)
        %[mean2(backim) std2(backim)]
        temp =  (temp.*(1-MaskAlpha) ) + (backim.* (MaskAlpha));
        %imshow(temp)
       
        temp = temp-mean2(temp);
        temp = temp/std2(temp);
        temp = temp .* signalcontrast;
        temp = temp + LC(1); % [mean2(temp) std2(temp)] 
        backim = backim - mean2(backim); backim = backim/std2(backim); 
        backim = backim .* (1 - signalcontrast);
        backim = backim + LC(1); %[mean2(backim) std2(backim)]
        blendim = (temp + backim);%[mean2(backim) std2(backim)]
        blendim = blendim/std2(blendim); 
        
        %normalization to desired luminance and contrast
        corr = LC(2)/std2(blendim); blendim = blendim*corr;
        corr = LC(1)-mean2(blendim); blendim = blendim+corr;
        %imshow(blendim)
        %[mean2(blendim) std2(blendim)]
        backim = backy{thenois};
        blendim(MaskBack) = backim(MaskBack);
        %imshow(blendim)
        
        
        if thenois < 10
            noise = ['nf0' num2str(thenois)];
        else
            noise = ['nf' num2str(thenois)];
        end
        name = [noise '_' nim(theface).name];
        shiiBlend{thenois,theface} = blendim;
        imwrite(blendim,[outfolder name],'BMP')
    end
    imwrite(backim,[noisefolder noise],'BMP')
    
    %imshow(backim)
end


for times = 20:120
    imshow(cell2mat(shiiBlend(2,times))); pause (0.5)
    imshow(cell2mat(backy(2))); pause (0.5)
end
