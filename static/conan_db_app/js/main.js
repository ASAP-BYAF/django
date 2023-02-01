// ページ読み込み時にページネーションで別ページがある場合には
// フォームの値をクエリパラメータに設定して、
// ページネーションで用意された別のページに遷移しても
// フォームで指定した種類のみでページネーションが行われるようにする。

// 前のページがあるときの処理が未設定。

// window.addEventListener("load", setQueryParam);

// フォーム要素を取得。
const valueRefineQuestionForm = document.querySelector('#refine-question-form');

function setQueryParam(event) {
  // 現在、選択されている分類の値を取得
  const valueKind = valueRefineQuestionForm.kind.value;
  const valueJenre = valueRefineQuestionForm.jenre.value;

  console.log(valueKind);
  console.log(valueJenre);

  // 遷移先の url が書かれている要素を取得
  const url_prev = document.getElementById('question-list-page-prev');
  const url_first = document.getElementById('question-list-page-first');
  const url_next = document.getElementById('question-list-page-next');
  const url_last = document.getElementById('question-list-page-last');

  // 前のページがあるときにのみ prev と first の url に対してクエリパラメータの設定を行う。
  if (url_prev) {
    // 遷移先の url のクエリパラメータに form に設定されている値を追加。
    console.log(url_prev);
    console.log(url_prev.getAttribute('href'));
    console.log(url_first);
    console.log(url_first.getAttribute('href'));
    const url_prev_with_query = url_prev.getAttribute('href') 
      + '&jenre=' + valueJenre
      + '&kind=' + valueKind;
    const url_first_with_query = url_first.getAttribute('href') 
      + '&jenre=' + valueJenre
      + '&kind=' + valueKind;
    url_prev.setAttribute('href', url_prev_with_query);
    url_first.setAttribute('href', url_first_with_query);
  }

  // 次のページがあるときにのみ next と last の url に対してクエリパラメータの設定を行う。
  if (url_next) {
    // 遷移先の url のクエリパラメータに form に設定されている値を追加。
    console.log(url_next);
    console.log(url_next.getAttribute('href'));
    console.log(url_last);
    console.log(url_last.getAttribute('href'));
    const url_next_with_query = url_next.getAttribute('href') 
      + '&jenre=' + valueJenre
      + '&kind=' + valueKind;
    const url_last_with_query = url_last.getAttribute('href') 
      + '&jenre=' + valueJenre
      + '&kind=' + valueKind;
    url_next.setAttribute('href', url_next_with_query);
    url_last.setAttribute('href', url_last_with_query);
  }
}


console.log();

function plusPageAndSendForm(page) {
  document.refine_form.action += page + '/';
  document.refine_form.submit();
}

function openCloseForm(id){
  console.log(id);
  // 与えられた id の次の要素の表示非表示を切り替える
  const target_oc_btn = document.getElementById(id); // 切り替えるボタン要素を取得
  openClose(target_oc_btn, target_oc_btn.nextElementSibling);
}

window.addEventListener("load", ifChecked());
window.addEventListener("load", ifTyped());

// チェックボックス形式のフォームについて一つでもチェックが入っていれば
// フォーム全体を表示、一つもチェックが入っていなければ、非表示にする。
function ifChecked(){
  const refine_check = countClass('refine-check');
  for (let i=0; i<refine_check.length; i++) {
    target_check = refine_check[i]; // 選択肢リストが入った <div> 
    const child_nodes_count = target_check.childElementCount;
    for(let j=0; j<child_nodes_count; j++) {
      if (target_check.children[j].firstElementChild.checked){
        openClose(target_check.previousElementSibling, target_check)
        break;
      }
    }
  }
}

function ifTyped(){
  const refine_type = countClass('refine-type');
  for (let i=0; i<refine_type.length; i++) {
    target_type = refine_type[i]; // 選択肢リストが入った <div> 
    const child_nodes_count = target_type.childElementCount;
    for(let j=0; j<child_nodes_count; j++) {
      if (target_type.children[j].firstElementChild.value.trim()){
        openClose(target_type.previousElementSibling, target_type)
        console.log(target_type.children[j].firstElementChild.value);
        break;
      }
    }
  }
}

function openClose(tgt, tgt2){
  const stat = tgt.textContent
  if(stat=="＋"){
    tgt.textContent = "－";
    tgt2.style.display= "block";
  }
  if(stat=="－"){
    tgt.textContent = "＋";
    tgt2.style.display= "none";
  }  
}

function countClass(cls_name){
  const num_cls_name = document.getElementsByClassName(cls_name);
  return num_cls_name;
}