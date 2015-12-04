from make_configs import makeConfigs

# Run tests on ialu and imult
makeConfigs("ialu_imult_test", 
	{'res:ialu': range(1,15), 'res:imult': range(1,15)},
	{}
)
