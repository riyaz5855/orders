// // download pdf--------------------------------------------------------------------------------------

// <!-- Include pdfmake and html2canvas -->
// <script src="https://cdnjs.cloudflare.com/ajax/libs/pdfmake/0.2.2/pdfmake.min.js"></script>
// <script src="https://cdnjs.cloudflare.com/ajax/libs/pdfmake/0.2.2/vfs_fonts.js"></script>
// <script src="https://html2canvas.hertzen.com/dist/html2canvas.min.js"></script>

// <!-- Your button element -->
// <button id="spdf">Create PDF</button>

// <!-- Your JavaScript code -->
// <script>
//   const button = document.getElementById("spdf");

//   button.addEventListener("click", () => {
//     // Get the HTML content of the page
//     const html = document.documentElement;

//     // Convert the HTML to a pdfmake-compatible format using html2canvas
//     html2canvas(html).then(canvas => {
//       const imgData = canvas.toDataURL('image/png');
//       const pdfWidth = canvas.width * 0.75;
//       const pdfHeight = canvas.height * 0.75;
//       const pdf = {
//         pageSize: { width: pdfWidth, height: pdfHeight },
//         content: [
//           {
//             image: imgData,
//             width: pdfWidth,
//           }
//         ]
//       };
//       pdfMake.createPdf(pdf).download('page.pdf');
//     });
//   });
// </script>


