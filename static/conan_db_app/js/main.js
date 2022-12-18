valueRefineQuestionForm.addEventListener('change', handleChange);

function handleChange(event) {
  // 現在の選択状態を取得
  const valueKind = valueRefineQuestionForm.kind.value;
  const valueJenre = valueRefineQuestionForm.jenre.value;

  console.log(valueKind)
  console.log(valueJenre)
}

