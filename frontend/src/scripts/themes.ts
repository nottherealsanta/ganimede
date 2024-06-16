export const light_theme: any = {
  "base": "vs",
  "inherit": true,
  "rules": [
    { token: '', foreground: '020418', background: 'fffffe' },
		{ token: 'invalid', foreground: 'cd3131' },
		{ token: 'emphasis', fontStyle: 'italic' },
		{ token: 'strong', fontStyle: 'bold' },

		{ token: 'variable', foreground: '001188' },
		{ token: 'variable.predefined', foreground: '4864AA' },
		{ token: 'constant', foreground: 'dd0000' },
		{ token: 'comment', foreground: '008000' },
		{ token: 'number', foreground: '09885A' },
		{ token: 'number.hex', foreground: '3030c0' },
		{ token: 'regexp', foreground: '800000' },
		{ token: 'annotation', foreground: '808080' },
		{ token: 'type', foreground: '008080' },

		{ token: 'delimiter', foreground: '000000' },
		{ token: 'delimiter.html', foreground: '383838' },
		{ token: 'delimiter.xml', foreground: '0000FF' },
    {token: 'delimiter.bracket', foreground: '000000'},

		{ token: 'tag', foreground: '800000' },
		{ token: 'tag.id.jade', foreground: '4F76AC' },
		{ token: 'tag.class.jade', foreground: '4F76AC' },
		{ token: 'meta.scss', foreground: '800000' },
		{ token: 'metatag', foreground: 'e00000' },
		{ token: 'metatag.content.html', foreground: 'FF0000' },
		{ token: 'metatag.html', foreground: '808080' },
		{ token: 'metatag.xml', foreground: '808080' },
		{ token: 'metatag.php', fontStyle: 'bold' },

		{ token: 'key', foreground: '863B00' },
		{ token: 'string.key.json', foreground: 'A31515' },
		{ token: 'string.value.json', foreground: '0451A5' },

		{ token: 'attribute.name', foreground: 'FF0000' },
		{ token: 'attribute.value', foreground: '0451A5' },
		{ token: 'attribute.value.number', foreground: '09885A' },
		{ token: 'attribute.value.unit', foreground: '09885A' },
		{ token: 'attribute.value.html', foreground: '0000FF' },
		{ token: 'attribute.value.xml', foreground: '0000FF' },

		{ token: 'string', foreground: 'b13541' },
		{ token: 'string.html', foreground: '0000FF' },
		{ token: 'string.sql', foreground: 'FF0000' },
		{ token: 'string.yaml', foreground: '0451A5' },

		{ token: 'keyword', foreground: '2965CC' },
		{ token: 'keyword.json', foreground: '0451A5' },
		{ token: 'keyword.flow', foreground: 'AF00DB' },
		{ token: 'keyword.flow.scss', foreground: '0000FF' },

		{ token: 'operator.scss', foreground: '666666' },
		{ token: 'operator.sql', foreground: '778899' },
		{ token: 'operator.swift', foreground: '666666' },
		{ token: 'predefined.sql', foreground: 'FF00FF' },


  ],
  "colors": {
    "editor.foreground": "#000000",
    "editor.background": "#FCFCFD",
    "editor.selectionBackground": "#BAD6FD",
    "editor.lineHighlightBackground": "#00000012",
    "editorCursor.foreground": "#000000",
    "editorWhitespace.foreground": "#BFBFBF",
		"editorBracketHighlight.foreground1": "#005CC6",
    "editorBracketHighlight.foreground2": "#008001",
		"editorBracketHighlight.foreground3": "#5B32A3",
    "editorBracketHighlight.unexpectedBracket.foreground": "#ff0000",
	}
}