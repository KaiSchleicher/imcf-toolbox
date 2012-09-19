%
%  Filaments Sandbox for Imaris 7
%

function XTGetFilaments()
	ver = 28
	
	% start Imaris and set up the connection
	conn = IceImarisConnector();
	conn.startImaris();

	% wait until the connection is ready and the user has selected some data
	ans = questdlg('Click "OK" to contine after opening a dataset and selecting a Filament object.', 'Waiting for Imaris...', 'OK', 'Cancel', 'OK')
	switch ans
		case 'OK'
			extractFilaments(conn.mImarisApplication);
	end
end

function extractFilaments(vImApp)
	vFactory = vImApp.GetFactory;
	vFilaments = vFactory.ToFilaments(vImApp.GetSurpassSelection);
	vSurpassScene = vImApp.GetSurpassScene;

	if ~vFactory.IsFilaments(vFilaments)
		for vChildIndex = 1:vSurpassScene.GetNumberOfChildren
			vDataItem = vSurpassScene.GetChild(vChildIndex - 1);
			if vFactory.IsFilaments(vDataItem)
				vFilaments = vFactory.ToFilaments(vDataItem);
				break;
			end
		end
		
		% check if there was a filament at all
		if isequal(vFilaments, [])
			msgbox('Could not find any Filaments!');
			return;
		end
	end
		
	vFilamentsXYZ = vFilaments.GetPositionsXYZ(0);
	vFilamentsXYZ

	csvwrite('h:\bla.csv', vFilamentsXYZ)
end