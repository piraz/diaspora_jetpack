(function($, can) {
	'use strict';

	var contacts = new can.List([{
		name: 'Fulano de Tal',
		online: true
	}, {
		name: 'Beltrano',
		online: false
	}, {
		name: 'Joãozinho',
		online: true
	}]);

	var totalOnline = can.compute(function() {
		var online = 0;

		contacts.each(function(contact) {
			if (contact.attr("online")) {
				online++;
			}
		});

		return online;
	});

	var frag = can.view('#dc-chat', {
		contacts: contacts,
		totalOnline: totalOnline
	});

	$('body').append(frag);
})(window.jQuery, window.can);