var updateBtns = document.getElementsByClassName('update-cart2')
for (var i = 0; i < updateBtns.length; i++){
    updateBtns[i].addEventListener('click',function () {
         var productId = this.dataset.id
         var action = this.dataset.action
         let model = this.dataset.model
         var id_quantity = 1
        if (document.getElementById("id_quantity")) {
            id_quantity = document.getElementById("id_quantity").options.selectedIndex + 1;
        }
        //  console.log('productID:', productId, "action:", action, "model: ", model, "qwy", id_quantity);
        updateUserOrder(productId, action, id_quantity)
        // }else{
        //     updateUserOrder(productId, action)
        // }
     });
 }

 function updateUserOrder(productId, action, quantity){
    // console.log('User is logged in')

     var url = '/cart/update_item/'

     fetch(url, {
         method: 'POST',
         headers:{
             'Content-Type': 'application/json',
             'X-CSRFToken': csrftoken,
             // credentials: 'include',
         },
         body:JSON.stringify({'productId': productId, 'action': action, 'quantity': quantity})
     })
         .then((response) => {
             return response.json()
         })
         .then((data) => {
             console.log('data:', data)
             location.reload()
         })
 }
 function chpok(id){
    elem = document.getElementById(id); //находим блок div по его id, который передали в функцию
    state = elem.style.display; //смотрим, включен ли сейчас элемент
    if (state =='') elem.style.display='none'; //если включен, то выключаем
    else elem.style.display=''; //иначе - включаем
}
