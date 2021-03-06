%
%  Surfaces to STL Exporter for Imaris 7 by Niko Ehrenfeuchter
%
%  Requirements:
%	- IceImarisConnector (https://github.com/aarpon/IceImarisConnector)
%
%%% Imaris meta information %%%
% <CustomTools>
%  <Menu>
%   <Submenu name="Surfaces Functions">
%	<Item name="Surfaces to STL Exporter" icon="Matlab"
%	   tooltip="Export selected Surfaces to STL.">
%	  <Command>MatlabXT::IceXTSurfacesToSTL(%i)</Command>
%	</Item>
%   </Submenu>
%  </Menu>
%  <SurpassTab>
%	<SurpassComponent name="bpSurfaces">
%	  <Item name="Export Surfaces to STL">
%		<Command>MatlabXT::IceXTSurfacesToSTL(%i)</Command>
%	  </Item>
%	</SurpassComponent>
%  </SurpassTab>
% </CustomTools>

function IceXTSurfacesToSTL(mImarisApplication)
	ver = 12;	% internal version number
	
	if nargin == 1
        javaaddpath ImarisLib.jar;
		% mImarisApplication
		conn = IceImarisConnector(mImarisApplication);
    else
        % start Imaris and set up the connection
		conn = IceImarisConnector();
		conn.startImaris();
	end

	% if called from matlab using an existing connection (useful for
	% debugging), it is better to do some sanity checks first:
	if ~conn.isAlive
		fprintf('Error: no connection to Imaris!\n');
		return;
	end
	vImApp = conn.mImarisApplication;
	fprintf('connection ID: %s\n', char(vImApp));
	while ~vImApp.GetFactory.IsSurfaces(vImApp.GetSurpassSelection)
		msg = 'Select a SURFACE object in Imaris!';
		title = 'Selection required';
		ans = questdlg(msg, title, 'OK', 'Cancel', 'OK');
		if strcmp(ans, 'Cancel')
			return;
		end
	end

	exportSurfacesToSTL(conn.mImarisApplication);
end


function exportSurfacesToSTL(vImApp)
	vFactory = vImApp.GetFactory;
	vSurfaces = vFactory.ToSurfaces(vImApp.GetSurpassSelection);
	% notification steps in percentage
	psteps = [ 1 5 10 25 50 75 ];

	vFileName = vImApp.GetCurrentFileName;
	[fpath, fname, ext] = fileparts(char(vFileName));
	[fname, fpath] = uiputfile(fullfile(fpath, ...
		[fname '-surfaces.stl']), ...
		'File name for the surface export');
	if fname == 0
		fprintf('aborting due to user request\n');
		return;
	end
	fprintf('writing STL format to "%s"\n\n', [fpath fname]);
	fid = fopen([fpath fname], 'w');

	t_all = tic;
	for SurfaceID = 0:(vSurfaces.GetNumberOfSurfaces - 1)
		vTri = vSurfaces.GetTriangles(SurfaceID);
		vNormals = vSurfaces.GetNormals(SurfaceID);
		vVertices = vSurfaces.GetVertices(SurfaceID);

		fprintf('--> processing surface %i (%i triangles)\n', ...
			SurfaceID, length(vTri));

		% calculate the index numbers for the given percentages
		nsteps = psteps * round(length(vTri) / 100);

		t0 = tic;
		fprintf(fid, 'solid imssurface-%i\n', SurfaceID);
		for tri = 1:length(vTri)
			% nid is the index of the current triangle in the nsteps array
			nid = find(nsteps == tri);
			if nid
				fprintf('%i%% completed: %i triangles, ', psteps(nid), tri);
				to_go = toc(t0) * (100 / psteps(nid) - 1);
				fprintf('est. time remaining: %.1fs\n', to_go);
			end
			vi = vTri(tri,:) + 1; % indices of vertices
			% calculate the facet normal (fn):
			fn = sum(vNormals(vi,:));
			fn = fn / norm(fn);
			tv = vVertices(vi,:); % triangle vertices
			fprintf(fid, ['  facet normal ' num2str(fn, '%e %e %e') '\n' ...
			'    outer loop\n' ...
			'      vertex ' num2str(tv(1,:), '%e %e %e') '\n' ...
			'      vertex ' num2str(tv(2,:), '%e %e %e') '\n' ...
			'      vertex ' num2str(tv(3,:), '%e %e %e') '\n' ...
			'    endloop\n' ...
			'  endfacet\n']);
		end
		fprintf(fid, 'endsolid imssurface-%i\n', SurfaceID);
		fprintf('surface %i done, time: %.1fs\n', SurfaceID, toc(t0));
	end % for SurfaceID
	fclose(fid);
	fprintf('\n==> done exporting %i surfaces in %.1fs\n', ...
		vSurfaces.GetNumberOfSurfaces, toc(t_all));
end % exportSurfacesToSTL
