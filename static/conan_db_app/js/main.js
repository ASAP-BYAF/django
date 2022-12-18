const valueRefineQuestionForm = document.querySelector('#refine-question-form');

valueRefineQuestionForm.addEventListener('change', handleChange);

function handleChange(event) {
  // 現在の選択状態を取得
  const valueKind = valueRefineQuestionForm.kind.value;
  const valueJenre = valueRefineQuestionForm.jenre.value;

  console.log(valueKind)
  console.log(valueJenre)
}

const url = new URL(location);
url.toString();

// if( !url.searchParams.get('mode') ) {

// 	url.searchParams.append('mode','view');
// 	location.href = url;

// } else {
// 	console.log(url.searchParams.get('mode')); // view
// }
