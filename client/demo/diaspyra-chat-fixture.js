can.fixture({
	'GET /contacts': function() {
		return [{
			id: 1,
			name: 'Fulano de Tal',
			online: true
		}, {
			id: 2,
			name: 'Beltrano',
			online: false
		}, {
			id: 3,
			name: 'Joãozinho',
			online: true
		},
		{
			id: 4,
			name: 'Pedrinho',
			online: true
		},
		{
			id: 5,
			name: 'José',
			online: true
		},
		{
			id: 6,
			name: 'Outro ai',
			online: true
		}];
	}
});

can.fixture.delay = 2000; // Delay time to server reply