***************************************
Integração do VLibras News API no Plone
***************************************

.. contents:: Conteúdo
   :depth: 2

Introdução
-----------

Este pacote integra no Plone o VLibras News API,
um serviço desenvolvido pelo `Laboratório de Aplicações de Video Digital <http://lavid.ufpb.br/>`_ para gerar vídeo de `LIBRAS <http://vlibras.gov.br/>`_ .

Este pacote suporta somente tipos de conteúdo Dexterity.

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

4. Acesse o painel de controle e instale o produto **.gov.br: Tradução de Português para Libras**.

Uso
---

TBD.
