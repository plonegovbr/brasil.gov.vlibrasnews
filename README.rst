***************************************************************
`.gov.br: Tradução de Português para Libras`
***************************************************************

.. contents:: Conteúdo
   :depth: 2

Introdução
-----------

Este pacote integra o VLibras News API, desenvolvido pelo `Laboratório de Aplicações de Video Digital - LAViD`_, um Tradutor de Português para Libras para Plone.


Estado deste pacote
---------------------

O **brasil.gov.vlibrasvideo** tem testes automatizados e, a cada alteração em seu
código os testes são executados pelo serviço Travis.

O estado atual dos testes pode ser visto nas imagens a seguir:

.. image:: http://img.shields.io/pypi/v/brasil.gov.vlibrasvideo.svg
    :target: https://pypi.python.org/pypi/brasil.gov.vlibrasvideo

.. image:: https://img.shields.io/travis/plonegovbr/brasil.gov.vlibrasvideo/master.svg
    :target: http://travis-ci.org/plonegovbr/brasil.gov.vlibrasvideo

.. image:: https://img.shields.io/coveralls/plonegovbr/brasil.gov.vlibrasvideo/master.svg
    :target: https://coveralls.io/r/plonegovbr/brasil.gov.vlibrasvideo

.. warning:: Neste momento utilizamos a versão 1.0 do plone.app.contenttypes.
             A versão 1.1a1 introduziu mudanças na maneira como o Plone trabalha com Eventos.

Instalação
------------

Para habilitar a instalação deste produto em um ambiente que utilize o
buildout:

1. Editar o arquivo buildout.cfg (ou outro arquivo de configuração) e
   adicionar o pacote ``brasil.gov.vlibrasvideo`` à lista de eggs da instalação::

        [buildout]
        ...
        eggs =
            brasil.gov.vlibrasvideo

2. Após alterar o arquivo de configuração é necessário executar
   ''bin/buildout'', que atualizará sua instalação.

3. Reinicie o Plone

4. Acesse o painel de controle e instale o produto
**.gov.br: Tradução de Português para Libras**.

.. _`Laboratório de Aplicações de Video Digital - LAViD`: http://lavid.ufpb.br/
