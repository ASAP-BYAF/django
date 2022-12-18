// alert("Hello! I am an alert box!!");

console.log(1);

// const element = document.querySelector('#id_kind');
// const value = element.value;
// console.log(value);

// let element = document.getElementById('id_kind');
// console.log(element.value);

// const element = document.querySelector('#id_kind');
const valueRefineQuestionForm = document.querySelector('#refine-question-form');
// 変更イベントを監視
// element.addEventListener('change', handleChange());
// element.addEventListener('change', () => console.log(element.value));
// form要素を参照
// const element = document.querySelector('#radioGroup');
// 変更を監視
valueRefineQuestionForm.addEventListener('change', handleChange);

function handleChange(event) {
  // 現在の選択状態を取得
  const valueKind = valueRefineQuestionForm.kind.value;
  const valueJenre = valueRefineQuestionForm.jenre.value;

  console.log(valueJenre)
}

