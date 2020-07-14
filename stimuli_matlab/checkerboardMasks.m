%make checkerboard masks for face and background
close all; clear all
basefolder = '/home/jschuurmans/Documents/02_recurrentSF_3T/Stimuli/JOLIEN_STIM_MAIN/';
imagefolder = '/home/jschuurmans/Documents/02_recurrentSF_3T/Stimuli/JOLIEN_STIM_MAIN/stimuli/';
outfolder = '/home/jschuurmans/Documents/02_recurrentSF_3T/Stimuli/JOLIEN_STIM_MAIN/';
basefolder = '/home/jschuurmans/Documents/02_recurrentSF_3T/Stimuli/JOLIEN_STIM_MAIN/';


finalSize = [550,550]
[MaskIm,~,MaskAlpha] = (imread([basefolder 'blurrymask.png']));
MaskAlpha = single(MaskAlpha); MaskAlpha = imresize(MaskAlpha, finalSize);
MaskAlpha = MaskAlpha./max(MaskAlpha(:));

blobFinding = MaskAlpha; % need to use a mask to only select face pixels, give them the same LC as the face

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
MaskIm = ~MaskBack;

imshow(MaskIm)
imshow(MaskBack)

imwrite(MaskIm,[outfolder 'MaskIm'],'BMP')
imwrite(MaskBack,[outfolder 'MaskBack'],'BMP')