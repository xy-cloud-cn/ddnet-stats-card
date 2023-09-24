let preview = document.getElementById("preview");
let generate_url = document.createElement("div");
generate_url.id = "generate_url";
generate_url.className = "generate_url";
generate_url.innerText = window.location.protocol+'//'+window.location.host + '/svg';
preview.appendChild(generate_url);

let generate_btn = document.createElement("div");
generate_btn.id = "generate_btn";
generate_btn.className = "generate";
generate_btn.innerText = "Click to generate/点击生成";
preview.appendChild(generate_btn);
generate_btn.addEventListener("click", generate);

let copy_url_btn=document.createElement("div")
copy_url_btn.id="copy_url_btn"
copy_url_btn.innerHTML='<svg xmlns="http://www.w3.org/2000/svg" height="1em" viewBox="0 0 448 512"><!--! Font Awesome Free 6.4.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2023 Fonticons, Inc. --><style>svg{fill:#ffffff}</style><path d="M384 336H192c-8.8 0-16-7.2-16-16V64c0-8.8 7.2-16 16-16l140.1 0L400 115.9V320c0 8.8-7.2 16-16 16zM192 384H384c35.3 0 64-28.7 64-64V115.9c0-12.7-5.1-24.9-14.1-33.9L366.1 14.1c-9-9-21.2-14.1-33.9-14.1H192c-35.3 0-64 28.7-64 64V320c0 35.3 28.7 64 64 64zM64 128c-35.3 0-64 28.7-64 64V448c0 35.3 28.7 64 64 64H256c35.3 0 64-28.7 64-64V416H272v32c0 8.8-7.2 16-16 16H64c-8.8 0-16-7.2-16-16V192c0-8.8 7.2-16 16-16H96V128H64z"/></svg>'
copy_url_btn.addEventListener("click", copy_url);
generate_url.appendChild(copy_url_btn)
function copy_url() {
    let url = document.getElementById("generate_url").innerText;
    navigator.clipboard.writeText(url);
    copy_url_btn.innerHTML='<svg xmlns="http://www.w3.org/2000/svg" height="1em" viewBox="0 0 448 512"><!--! Font Awesome Free 6.4.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2023 Fonticons, Inc. --><style>svg{fill:#ffffff}</style><path d="M438.6 105.4c12.5 12.5 12.5 32.8 0 45.3l-256 256c-12.5 12.5-32.8 12.5-45.3 0l-128-128c-12.5-12.5-12.5-32.8 0-45.3s32.8-12.5 45.3 0L160 338.7 393.4 105.4c12.5-12.5 32.8-12.5 45.3 0z"/></svg>'
    setTimeout(() => copy_url_btn.innerHTML='<svg xmlns="http://www.w3.org/2000/svg" height="1em" viewBox="0 0 448 512"><!--! Font Awesome Free 6.4.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2023 Fonticons, Inc. --><style>svg{fill:#ffffff}</style><path d="M384 336H192c-8.8 0-16-7.2-16-16V64c0-8.8 7.2-16 16-16l140.1 0L400 115.9V320c0 8.8-7.2 16-16 16zM192 384H384c35.3 0 64-28.7 64-64V115.9c0-12.7-5.1-24.9-14.1-33.9L366.1 14.1c-9-9-21.2-14.1-33.9-14.1H192c-35.3 0-64 28.7-64 64V320c0 35.3 28.7 64 64 64zM64 128c-35.3 0-64 28.7-64 64V448c0 35.3 28.7 64 64 64H256c35.3 0 64-28.7 64-64V416H272v32c0 8.8-7.2 16-16 16H64c-8.8 0-16-7.2-16-16V192c0-8.8 7.2-16 16-16H96V128H64z"/></svg>', 1000)
}
function render_card(username, team, skin) {
    let xhr = new XMLHttpRequest();
    xhr.open('GET', '/svg?username=' + username + '&team=' + team + '&skin=' + skin, true);
    xhr.onload = function () {
        if (xhr.status === 200) {
            let svg = xhr.responseXML.documentElement;
            document.getElementsByClassName('card-preview')[0].appendChild(svg);
        }
    };
    xhr.send();
}

function render_skin_list() {
    //获取json数据
    let xhr = new XMLHttpRequest();
    xhr.open("GET", "/skinjson", true);
    xhr.responseType = "json";
    xhr.onload = function () {
        if (xhr.status === 200) {
            //解析成对象
            let skins = xhr.response.skins;
            let fathertree = document.getElementById('inputform')
            //创建table元素
            let table = document.createElement("table");
            table.id = 'myTable'
            //遍历每个皮肤信息
            for (let skin of skins) {
                //创建tr元素
                let tr = document.createElement("tr");
                tr.onclick = function () {
                    selectRow(this);
                };
                tr.style.backgroundColor = "#462753";
                tr.style.color = "white";
                //创建第一个td元素
                let td1 = document.createElement("td");
                //创建canvas元素
                let canvas = document.createElement("canvas");
                canvas.width = 96;
                canvas.height = 64;
                //调用RenderSkin函数
                let img = new Image();
                if (skin.type === "normal") {
                    //如果是normal类型，使用原来的URL
                    img.src = "https://ddnet.org/skins/skin/" + skin.name + ".png";
                } else if (skin.type === "community") {
                    //如果是community类型，使用新的URL
                    img.src = "https://ddnet.org/skins/skin/community/" + skin.name + ".png";
                }

                img.onload = function () {
                    OnTeeSkinRender(canvas, img);
                };
                //将canvas元素添加到td1中
                td1.appendChild(canvas);
                //创建第二个td元素
                let td2 = document.createElement("td");
                //创建文本节点
                let text = document.createTextNode(skin.name);
                //将文本节点添加到td2中
                td2.appendChild(text);
                //将两个td元素添加到tr中
                tr.appendChild(td1);
                tr.appendChild(td2);
                //将tr元素添加到table中
                table.appendChild(tr);
            }
            //将table元素添加到显示位置
            fathertree.appendChild(table);
            var input = document.getElementById("searchInput");
            var rows = table.rows;
            var cells;

            input.addEventListener("keyup", searchTable);

            function searchTable() {
                var keyword = input.value.toUpperCase();
                for (var i = 0; i < rows.length; i++) {
                    cells = rows[i].cells;
                    if (cells[1].innerHTML.toUpperCase().indexOf(keyword) > -1) {
                        rows[i].style.display = "";
                    } else {
                        rows[i].style.display = "none";
                    }
                }
            }
        }
    };
    xhr.send();


}

//定义一个全局变量，用来存储选中的行的数据
var selectedRowData = null;

//定义一个函数，用来选择表格中的一行
function selectRow(row) {
    //获取表格元素
    var table = document.getElementById("myTable");
    //获取表格中所有的行
    var rows = table.rows;
    //遍历所有的行
    for (var i = 0; i < rows.length; i++) {
        //取消所有已经选择的行的样式和状态
        rows[i].style.backgroundColor = "#462753";
        rows[i].style.color = "white";
        rows[i].setAttribute("data-selected", "false");
    }
    //为当前点击的行添加选中的样式和状态
    row.style.backgroundColor = "#ff5ef6";
    row.style.color = "white";
    row.setAttribute("data-selected", "true");
    //将当前点击的行的数据存储到变量中
    selectedRowData = row.cells[1].innerText;
}

render_skin_list()
render_card('nameless tee', '', 'default')

function generate() {
    let nickname = document.getElementsByName("nickname")[0].value;
    let team = document.getElementsByName("team")[0].value;
    let skin = selectedRowData;
    if (nickname === '') {
        nickname = 'nameless tee';
    }
    if (skin === null) {
        skin = 'default';
    }
    document.getElementsByClassName('card-preview')[0].innerHTML = '';
    generate_url.innerText = window.location.protocol+'//'+window.location.host + '/svg?username=' + nickname + '&team=' + team + '&skin=' + skin;
    generate_url.appendChild(copy_url_btn)
    render_card(nickname, team, skin)

}
