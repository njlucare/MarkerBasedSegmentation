
dirs = '/orange/pinaki.sarder/nlucarelli/intestine/';
downsample = 1;

stringsToSkip = {'.','..','B001_CL','B001_SB','B006_CL','B006_SB','B008_CL','B008_SB','B004_SB','B004_CL','B005_CL','B005_SB'};

cases = dir([dirs,'*/']);

for i = 1:length(cases)
    currentString = cases(i).name;
    
    if ismember(currentString, stringsToSkip)
          fprintf('Skipping: %s\n',currentString);
          continue   
    end
    
    current_dir = cases(i).folder;
    
    slides = dir([current_dir,'/',currentString,'/*RGB.tif']);
    if isempty(slides)
        slides = dir([current_dir,'/',currentString,'/*montage.tif']);
    end
    
    if isempty(slides)
        fprintf('Failed on: %s',currentString);
        break;
    end
    
    for j=1:length(slides)
        
        slide_name = [slides(j).folder,'/',slides(j).name];
        base_folder = strsplit(slide_name,'reg');
        slide_no = base_folder{2};
        slide_no = strsplit(slide_no,'_');
        slide_no = slide_no{1};
        base_folder = base_folder{1};
        
%         codex_name = [base_folder,'reg',slide_no,'_X01_Y01_Z01.tif'];
%         fprintf('Reading: %s\n',codex_name);
%         codex = tiffreadVolume(codex_name,'PixelRegion',{[1,downsample,inf],[1,downsample,inf],[1,1]});
%         im_bin = imbinarize(im2double(codex));
%         im_split = split_nuclei_functional2(im_bin);
        
        mask_nm = [base_folder,'reg',slide_no,'_mask.tif'];
        mask = tiffreadVolume(mask_nm,'PixelRegion',{[1,downsample,inf],[1,downsample,inf],[1,1]});
        mask = mask > 0;
        
        class_name = [base_folder,'reg',slide_no,'_classes.tif'];
        class_im = tiffreadVolume(class_name,'PixelRegion',{[1,downsample,inf],[1,downsample,inf],[1,1]});
        class_bin = class_im > 0;
        class_bin = imopen(class_bin,strel('disk',2));
        mn_dt=bwdist(class_bin);
        mn_w=watershed(mn_dt);
        ridgelines=mn_w==0;

        guided_watershed=imimposemin(mn_dt,ridgelines|class_bin);
        L=watershed(guided_watershed);
        segmented_nuclei=mask-(L==0)>0;
        segmented_nuclei=bwareaopen(segmented_nuclei,25);
        segmented_nuclei=imopen(segmented_nuclei,strel('disk',1));
        
%         mask2 = split_nuclei_functional2(mask);
        
        im_split = bwlabel(segmented_nuclei);
        im_split = uint16(im_split);
        save_name_base = strsplit(slide_name,'.tif');
        save_name_base = save_name_base{1};
        save_name = [save_name_base,'-labels.tif'];
        imwrite(im_split,save_name);

    end
    
end

