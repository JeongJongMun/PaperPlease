// 현재 선택된 LLM 모델을 저장할 변수
var selectedLLMModel = '';

// LLM 모델 버튼 클릭 이벤트 핸들러
function onClickLLMButton(model) {
    // 선택된 LLM 모델 변수 업데이트
    selectedLLMModel = model;

    // 원하는 작업 수행 (예: 모델 변경 시 어떤 동작 수행)
    console.log('Selected LLM Model:', selectedLLMModel);
}

async function question() {
    let input = $('#queryInput').val();
    $('#queryInput').val('');
    let _data = JSON.stringify({"input": input});
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
            $('#queryOutput').append(tempHtml);
        }, 
        error: function (error) {
            console.log(error);
        }
    });
}

// async function question() {
//     let input = $('#queryInput').val();
//     $('#queryInput').val('');
//     let _data = JSON.stringify({ "input": input });
//     console.log(_data);

//     $.ajax({
//         type: "POST",
//         url: "/chat/stream",
//         data: _data,
//         contentType: 'application/json',
//         success: function (response) {
//             // 데이터 구분하기
//             var lines = response.split('\n');
//             console.log(lines.length);
//             for (var i = 0; i < lines.length; i += 3) {
//                 if (lines[i].includes("event: end")) {
//                     let tempHtml = '</div>';
//                     $('#queryOutput').append(tempHtml);
//                     return;
//                 }
//                 else if (lines[i].includes("event: metadata")) {
//                     let tempHtml = '<div class="chat-bubble">'
//                     $('#queryOutput').append(tempHtml)
//                 }
//                 else if (lines[i].includes("event: data")) {
//                     var data = JSON.parse(lines[i + 1].replace('data: ', ''));
//                     console.log(data['content']);
//                     // IIFE를 사용하여 data 변수의 현재 값을 setTimeout에 전달
//                     (function(data) {
//                         setTimeout(function() {
//                             $('#queryOutput').append(data['content']);
//                         }, 3000);
//                     })(data);
//                 }
//             }

//         }
//     });
// }




function clearAnswers() {
    // queryOutput 요소를 찾아서 모든 하위 요소를 삭제
    var queryOutput = document.getElementById('queryOutput');
    while (queryOutput.firstChild) {
        queryOutput.removeChild(queryOutput.firstChild);
    }
}