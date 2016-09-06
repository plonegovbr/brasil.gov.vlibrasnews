***************************************
Integração do VLibras News API no Plone
***************************************

.. contents:: Conteúdo
   :depth: 2

Introdução
-----------

O VLibras News API é um serviço desenvolvido pelo `Laboratório de Aplicações de Video Digital <http://lavid.ufpb.br/>`_ para gerar traduções para `LIBRAS <http://vlibras.gov.br/>`_ em forma de vídeos armazenados no YouTube.

Este pacote é uma integração do VLibras News API no Plone,
atraves de um behavior para tipos de conteúdo Dexterity.

Estado deste pacote
-------------------

.. image:: http://img.shields.io/pypi/v/brasil.gov.vlibrasnews.svg
    :target: https://pypi.python.org/pypi/brasil.gov.vlibrasnews

.. image:: https://img.shields.io/travis/plonegovbr/brasil.gov.vlibrasnews/master.svg
    :target: http://travis-ci.org/plonegovbr/brasil.gov.vlibrasnews

.. image:: https://img.shields.io/coveralls/plonegovbr/brasil.gov.vlibrasnews/master.svg
    :target: https://coveralls.io/r/plonegovbr/brasil.gov.vlibrasnews

Instalação
----------

Para habilitar a instalação deste produto em um ambiente que utilize o buildout:

1. Editar o arquivo buildout.cfg (ou outro arquivo de configuração) e
   adicionar o pacote ``brasil.gov.vlibrasnews`` à lista de eggs da instalação:

.. code-block:: ini

      [buildout]
      ...
      eggs =
          brasil.gov.vlibrasnews

2. Após alterar o arquivo de configuração é necessário executar ''bin/buildout'', que atualizará sua instalação.

3. Reinicie o Plone

4. Acesse o painel de controle e instale o produto **.gov.br: Tradução de Português para LIBRAS**.

Uso
---

Após instalar o pacote é preciso ir na 'Configuração do Site',
selecionar 'VLibras News API' nas 'Configurações de Complementos',
e informar o token de acesso.

Para ativar o behavior é necessário ir em 'Tipos de conteúdo Dexterity',
selecionar o tipo de conteúdo que será processado,
e habilitar o behavior 'VLibras News'.

Um novo campo de só leitura será disponibilizado para armazenar o endereço do vídeo com a tradução a LIBRAS do conteúdo processado.

Como funciona
-------------

Quando um usuário publicar um objeto de um tipo de conteúdo com o behavior habilitado,
uma requisição é feita na API para criar um vídeo com a tradução do conteúdo para LIBRAS.

A partir desse momento a API é consultada periodicamente para conhecer o estado do processamento do vídeo.
Quando o vídeo ficar pronto para visualização, um viewlet disponibiliza um player para assistir o video.

Caso o conteúdo for modificado,
o vídeo anterior é retirado e uma nova requisição é feita para criar um novo vídeo com a tradução do conteúdo atualizado para LIBRAS.

Caso o conteúdo for excluido,
uma requisição é feita para excluir também o vídeo com a tradução do conteúdo para LIBRAS.
