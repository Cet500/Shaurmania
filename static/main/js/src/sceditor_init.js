document.addEventListener('DOMContentLoaded', function() {
	// SCEditor init
	let textareas = document.querySelectorAll('textarea[name=rich_content]');
	textareas.forEach(function(textarea) {
		sceditor.create(textarea, {
			format: 'xhtml',
			plugins: 'undo',
			icons: 'monocons',
			locale: 'ru',
			charset: 'utf-8',
			spellcheck: true,
			emoticonsEnabled: false,
			fonts: "Comfortaa,Verdana",
			toolbar: "bold,italic,underline,strike|" +
				"left,center,right,justify|font,color|" +
				"removeformat|" +
				"bulletlist,orderedlist|" +
				"table|" +
				"code|" +
				"maximize,source",
			colors: '#000000,#44B8FF,#1E92F7,#0074D9,#005DC2,#00369B,#b3d5f4|' +
				'#444444,#C3FFFF,#9DF9FF,#7FDBFF,#68C4E8,#419DC1,#d9f4ff|' +
				'#666666,#72FF84,#4CEA5E,#2ECC40,#17B529,#008E02,#c0f0c6|' +
				'#888888,#FFFF44,#FFFA1E,#FFDC00,#E8C500,#C19E00,#fff5b3|' +
				'#aaaaaa,#FFC95F,#FFA339,#FF851B,#E86E04,#C14700,#ffdbbb|' +
				'#cccccc,#FF857A,#FF5F54,#FF4136,#E82A1F,#C10300,#ffc6c3|' +
				'#eeeeee,#FF56FF,#FF30DC,#F012BE,#D900A7,#B20080,#fbb8ec|' +
				'#ffffff,#F551FF,#CF2BE7,#B10DC9,#9A00B2,#9A00B2,#e8b6ef',
		});
	});

	// Добавляем обработчик события для форм, чтобы получить данные из SCEditor перед отправкой
	var forms = document.querySelectorAll('form');
	forms.forEach(function(form) {
		form.addEventListener('submit', function(event) {
			textareas.forEach(function(textarea) {
				var instance = sceditor.instance(textarea);
				if (instance) {
					// Обновляем значение textarea перед отправкой формы
					textarea.value = instance.val();
				}
			});
		});
	});

});