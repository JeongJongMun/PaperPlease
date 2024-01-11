// 현재 선택된 LLM 모델을 저장할 변수
var selectedLLMModel = 'GPT3';


// LLM 모델 버튼 클릭 이벤트 핸들러
function onClickLLMButton(model) {
    // 선택된 LLM 모델 변수 업데이트
    selectedLLMModel = model;
    var allButtons = document.querySelectorAll('.model-btn');
    
    allButtons.forEach(btn => {
        btn.classList.remove('btn-secondary');
        btn.classList.add('btn-outline-secondary');
    });

    document.getElementById(`${model}`).classList.add('btn-secondary');
    document.getElementById(`${model}`).classList.remove('btn-outline-secondary');

    // 원하는 작업 수행 (예: 모델 변경 시 어떤 동작 수행)
    console.log('Selected LLM Model:', selectedLLMModel);
}


async function question() {
    let input = $('#queryInput').val();
    var tt = `<div class="chat-bubble2">${input}</div>`;
    $('#queryOutput').append(tt);

    $('#queryInput').val('');
    let _data = JSON.stringify({"input":  {"input":input}});
    console.log(_data);

    $.ajax({
        type: "POST",
        url: "/chat/invoke",
        data: _data,
        contentType: 'application/json',
        success: function (response) {
            // agent = response['output']['output'];
            // chain = response['ouput'];
            // just chatmodel = response['output']['content'];
            var tempHtml = `<div class="chat-bubble">${response['output']['output']}</div>`;
            console.log(response['output']['output'])
            console.log(response)
            $('#queryOutput').append(tempHtml);
        }, 
        error: function (error) {
            console.log(error);
        }
    });
}


function clearAnswers() {
    // queryOutput 요소를 찾아서 모든 하위 요소를 삭제
    var queryOutput = document.getElementById('queryOutput');
    while (queryOutput.firstChild) {
        queryOutput.removeChild(queryOutput.firstChild);
    }
}