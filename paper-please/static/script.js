const LLM = {
    GPT3: "gpt3",
    GPT4: "gpt4",
    Cohere: "cohere",
};

async function question() {
    let input = $('#queryInput').val()
    $('#queryInput').val('')
    alert(input)
    $.ajax({
        type: "POST",
        url: "/submit",
        data: {question: input},
        success: function (response) {
            if (response['result'] == 'success') {
                console.log("Query Success", response['answer'])
                let tempHtml = `
                <p class="w-full p-2 border border-secondary border-2 rounded-2">${response['answer']}</p>
                `;
                $('#queryOutput').append(tempHtml)
            } else {
                alert('쿼리 실패')
            }
        }
    });
}