document.addEventListener('DOMContentLoaded', () => {
    const formCriarLote = document.getElementById('form-criar-lote');
    const listaLotes = document.getElementById('lista-lotes');

    formCriarLote.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const tipo = document.getElementById('tipo-lote').value;
        const prioridade = document.getElementById('prioridade-lote').value;

        const loteData = {
            tipo: tipo,
            prioridade: parseInt(prioridade),
            cod_funcionario: 1, 
            cod_lote_prazo: 7 
        };

        try {
            const response = await fetch('http://localhost:8000/lotes/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(loteData),
            });

            if (!response.ok) {
                throw new Error('Falha ao criar o lote');
            }

            const novoLote = await response.json();
            adicionarLoteNaLista(novoLote);
            formCriarLote.reset();
        } catch (error) {
            console.error('Erro:', error);
            alert('Erro ao criar o lote. Verifique o console.');
        }
    });

    function adicionarLoteNaLista(lote) {
        const li = document.createElement('li');
        li.innerHTML = `
            <strong>Lote #${lote.cod_lote}</strong> - Tipo: ${lote.tipo}
            <button onclick="processarLote(${lote.cod_lote})">Processar</button>
        `;
        listaLotes.appendChild(li);
    }
    
    window.processarLote = async (codLote) => {
        try {
            const response = await fetch(`http://localhost:8000/lotes/${codLote}/processar`, {
                method: 'POST',
            });
            
            const resultado = await response.json();
            alert(resultado.message);
        } catch (error) {
            console.error('Erro ao processar lote:', error);
            alert('Erro ao processar lote.');
        }
    };
});