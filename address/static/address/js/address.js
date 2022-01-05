django.jQuery(function () {
	django.jQuery('select.address').each(function() {
		const select = django.jQuery(this);
		const defaultValue = select.data('select2-default-value');
		const option = new Option(defaultValue, defaultValue, true, true);
    	select.append(option);
	});
	const apiKey = django.jQuery('select.address').data('select2-api-key');
	const categories = django.jQuery('select.address').data('select2-filter-categories')
	django.jQuery('select.address').select2({
		minimumInputLength: 5,
		allowClear: true,
		language: 'cs',
		placeholder: '---',
		ajax: {
			url: 'https://geocode-api.arcgis.com/arcgis/rest/services/World/GeocodeServer/suggest',
			dataType: 'json',
			data: function (params) {
				var query = {
					text: params.term,
					category: categories,
					token: apiKey,
					f: 'json',
				};
				return query;
			},
			processResults: function (data) {
				return {
					results: data.suggestions.map((suggestion) => ({
						text: suggestion.text,
						id: suggestion.text,
					})),
					pagination: {
						more: false,
					},
				};
			},
			delay: 250,
			cache: true
		},
	});

});
