#! /usr/bin/env python
#! -*- coding:utf-8 -*-

# Copyright (c) 2007, PediaPress GmbH
# See README.txt for additional licensing information.

import copy
import inspect
import re

from mwlib.advtree import AdvancedNode, removeNewlines
from mwlib.advtree import (Article, ArticleLink, Big, Blockquote, Book, BreakingReturn, CategoryLink, Cell, Center, Chapter,
                           Cite, Code,DefinitionDescription, DefinitionList, DefinitionTerm, Deleted, Div, Emphasized,
                           HorizontalRule, ImageLink, Inserted, InterwikiLink, Italic, Item, ItemList, LangLink, Link,
                           Math, NamedURL, NamespaceLink, Overline, Paragraph, PreFormatted, Reference, ReferenceList,
                           Row, Section, Small, Source, SpecialLink, Strike, Strong, Sub, Sup, Table, Teletyped, Text,
                           Underline, URL, Var)

from mwlib.treecleanerhelper import *


def tryRemoveNode(node):
    if node.parent is not None:
        node.parent.removeChild(node)
        return True


def _all(list):
    for item in list:
        if item == False:
            return False
    return True

def _any(list):
    for x in list:
        if x:
            return True
    return False


class TreeCleaner(object):

    """The TreeCleaner object cleans the parse tree to optimize writer ouput.

    All transformations should be lossless.

    """


    def __init__(self, tree, save_reports=False, nesting_strictness='loose'):
        """Init with parsetree.

        The input tree needs to be an AdvancedTree, generated by advtree.buildAdvancedTree
        """
        self.tree = tree
        # list of actions by the treecleaner
        # each cleaner method has to report its actions
        # this helps debugging and testing the treecleaner
        self.reports = []

        # reports are only saved, if set to True
        self.save_reports = save_reports

        # list of nodes which do not require child nodes
        self.childlessOK = [ArticleLink, BreakingReturn, CategoryLink, Cell, Chapter, Code,
                            HorizontalRule, ImageLink, InterwikiLink, LangLink, Link, Math,
                            NamedURL, NamespaceLink, ReferenceList, SpecialLink, Text, URL]

        # FIXME: not used currently. remove if this is not used soon. could be used as reference
        # list nodes that apply styles to their children
        # FIXME: Center node might be problematic. Center is a block node and not inline
        self.inlineStyleNodes = [Big, Center, Cite, Code, Deleted, Emphasized, Inserted, Italic,
                                 Overline, Small, Strike, Strong, Sub, Sup, Teletyped, Underline, Var]

        # USED IN fixNesting if nesting_strictness == 'loose'
        # keys are nodes, that are not allowed to be inside one of the nodes in the value-list
        # ex: pull image links out of preformatted nodes
        # fixme rename to ancestors
        self.forbidden_parents = {ImageLink:[PreFormatted, Reference],
                                  ItemList:[Div],
                                  Source:self.inlineStyleNodes,
                                  Paragraph:[Paragraph],
                                  DefinitionList:[Paragraph],
                                  }
        self.forbidden_parents[Source].append(PreFormatted)

        # when checking nesting, some Nodes prevent outside nodes to be visible to inner nodes
        # ex: Paragraphs can not be inside Paragraphs. but if the inner paragraph is inside a
        # table which itself is inside a paragraph this is not a problem
        self.outsideParentsInvisible = [Table]
        self.nesting_strictness = nesting_strictness # loose | strict

        
        # ex: delete preformatted nodes which are inside reference nodes,
        # all children off the preformatted node are kept
        self.removeNodes = {PreFormatted:[Reference], Cite:[Item, Reference]}

        
        # ex: some tags need to be swapped: center nodes have to be pulled out of underline nodes
        # e.g. but only if the center is a direct and only child
        self.swapNodesMap = { Center:[Underline, Emphasized]} # { ChildClass: [ParentClass, ParentClass2]}


        # list of css classes which trigger the removal of the node from the tree
        # the following list is wikipedia specific
        self.noDisplayClasses = ['dablink', 'editlink', 'metadata', 'noprint', 'portal', 'sisterproject']


        self.cell_splitter_params = {
            'maxCellHeight': (7*72) * 3/4 ,
            'lineHeight':  26,
            'charsPerLine': 40,
            'paragraphMargin': 2, # add 10 pt margin-safety after each node
            'imgHeight': 6, # approximate image height in units of lineHeights
            }


    def clean(self, cleanerMethods):
        """Clean parse tree using cleaner methods in the methodList."""
        cleanerList = []
        for method in cleanerMethods:
            f = getattr(self, method, None)
            if f:
                cleanerList.append(f)
            else:
                raise 'TreeCleaner has no method: %r' % method            

        # FIXME: performance could be improved, if individual articles would be cleaned
        # the algorithm below splits on the first level, if a book is found
        # --> if chapters are used, whole chapters are cleaned which slows things down
        
        if self.tree.__class__ == Book :
            children = self.tree.children
        else:
            children = [self.tree]

        for child in children:
            for cleaner in cleanerList:
                cleaner(child)
            
        #for child in self.tree.children:
        #    for cleaner in cleanerList:
        #        cleaner(child)



    def cleanAll(self, skipMethods=[]):
        """Clean parse tree using all available cleaner methods."""

        cleanerMethods = ['removeEmptyTextNodes',
                          'cleanSectionCaptions',
                          'removeChildlessNodes',
                          'removeLangLinks',
                          'removeListOnlyParagraphs',
                          'fixParagraphs', # was in xmltreecleaner
                          'fixNesting', 
                          'removeSingleCellTables',
                          'removeCriticalTables',
                          'removeBrokenChildren',
                          'fixTableColspans',
                          'moveReferenceListSection',
                          'removeBreakingReturns', # NEW
                          'removeEmptyReferenceLists',# NEW
                          'swapNodes',# NEW
                          'splitBigTableCells',# NEW
                          'removeNoPrintNodes',# NEW
                          'removeChildlessNodes', # methods above might leave empty nodes behind - clean up
                          'removeNewlines', # imported from advtree - clean up newlines that are not needed
                          'removeBreakingReturns', # NEW
                          'findDefinitionLists',
                          'fixNesting', # pull DefinitionLists out of Paragraphs
                          'removeChildlessNodes', 
                          ]
        self.clean([cm for cm in cleanerMethods if cm not in skipMethods])


    def report(self, *args):        
        if not self.save_reports:
            return
        caller = inspect.stack()[1][3]
        msg = ''
        if args:
            msg = ' '.join([repr(arg) for arg in args])        
        self.reports.append((caller, msg))        
        
    def getReports(self):
        return self.reports

    def removeNewlines(self, node):
        removeNewlines(node)

    def removeEmptyTextNodes(self, node):
        """Removes Text nodes which contain no text at all.

        Text nodes which only contain whitespace are kept.
        """
        
        if node.__class__ == Text:
            if not len(node.caption) and node.parent:
                self.report('removed empty text node')
                node.parent.removeChild(node)
                return
        for c in node.children:
            self.removeEmptyTextNodes(c)

    def removeListOnlyParagraphs(self, node):
        """Removes paragraph nodes which only have lists as the only childen - keep the lists."""
        if node.__class__ == Paragraph:
            list_only_children = _all([c.__class__ == ItemList for c in node.children])
            if list_only_children and node.parent:
                self.report('replaced children:', node, '-->', node.children, 'for node:', node.parent)
                node.parent.replaceChild(node, node.children)
                
        for c in node.children[:]:
            self.removeListOnlyParagraphs(c)


    def removeChildlessNodes(self, node):
        """Remove nodes that have no children except for nodes in childlessOk list."""   
        if not node.children and node.__class__ not in self.childlessOK:
            removeNode = node
            while removeNode.parent and not removeNode.siblings:
                removeNode = removeNode.parent
            if removeNode.parent:
                self.report('removed:', removeNode)
                removeNode.parent.removeChild(removeNode)
        for c in node.children[:]:
            self.removeChildlessNodes(c)
            

    def removeLangLinks(self, node):
        """Removes the language links that are listed below an article.

        Language links inside the article should not be touched
        """

        txt = []
        langlinkCount = 0

        for c in node.children:
            if c.__class__ == LangLink:
                langlinkCount +=1
            else:
                txt.append(c.getAllDisplayText())
        txt = ''.join(txt).strip()
        if langlinkCount and not txt and node.parent:
            self.report('removed child:', node)
            node.parent.removeChild(node)

        for c in node.children[:]:
            self.removeLangLinks(c)


    def _tableIsCrititcal(self, table):
        classAttr = table.attributes.get('class', '')
        if re.findall(r'\bnavbox\b', classAttr):    
            return True

        return False

    def removeCriticalTables(self, node):
        """Remove problematic table nodes - keep content.
               
        The content is preserved if possible and only the outmost 'container' table is removed.
        """

        if node.__class__ == Table and self._tableIsCrititcal(node):
            children = []
            for row in node.children:
                for cell in row:
                    for n in cell:
                        children.append(n)
            if node.parent:
                self.report('replaced child:', node, children)
                node.parent.replaceChild(node, children)
            return

        for c in node.children:
            self.removeCriticalTables(c)

    def fixTableColspans(self, node):
        """ Fix erronous colspanning information in table nodes.

        1. SINGLE CELL COLSPAN: if a row contains a single cell, the
           colspanning amount is limited to the maximum table width
        """

        # SINGLE CELL COLSPAN 
        if node.__class__ == Table:
            maxwidth = 0
            for row in node.children:
                numCells = len(row.children)
                rowwidth = 0
                for cell in row.children:
                    colspan = cell.attributes.get('colspan', 1)
                    if numCells > 1:
                        rowwidth += colspan
                    else:
                        rowwidth += 1
                maxwidth = max(maxwidth,  rowwidth)
            for row in node.children:
                numCells = len(row.children)
                if numCells == 1:
                    cell = row.children[0]
                    colspan = cell.attributes.get('colspan', 1)
                    if colspan and colspan > maxwidth:
                        self.report('fixed colspan from', cell.vlist.get('colspan', 'undefined'), 'to', maxwidth)
                        cell.vlist['colspan'] = maxwidth
                        
        # /SINGLE CELL COLSPAN
        for c in node.children:
            self.fixTableColspans(c)

    def removeBrokenChildren(self, node):
        """Remove Nodes (while keeping their children) which can't be nested with their parents."""
        if node.__class__ in self.removeNodes.keys():
            if _any([parent.__class__ in self.removeNodes[node.__class__] for parent in node.parents]):
                if node.children:
                    children = node.children
                    self.report('replaced child', node, children)
                    node.parent.replaceChild(node, newchildren=children)
                else:
                    self.report('removed child', node)
                    node.parent.removeChild(node)
                return

        for c in node.children:
            self.removeBrokenChildren(c)


    def removeSingleCellTables(self, node):
        """Remove table nodes which contain only a single row with a single cell"""

        if node.__class__ == Table:
            if len(node.children) == 1 and len(node.children[0].children) == 1:
                if node.parent:
                    cell_content = node.children[0].children[0].children
                    self.report('replaced Child', node, cell_content)
                    node.parent.replaceChild(node, cell_content)

        for c in node.children:
            self.removeSingleCellTables(c)


    def moveReferenceListSection(self, node):
        """Move the section containing the reference list to the end of the article."""

        if node.__class__ == Article:
            sections = node.getChildNodesByClass(Section)
            for section in sections:
                reflists = section.getChildNodesByClass(ReferenceList)
                if reflists and section.parent:
                    self.report('moving section', section, 'to', node)
                    section.parent.removeChild(section)
                    node.appendChild(section)
            return

        for c in node.children:
            self.moveReferenceListSection(c)

    # FIXME: replace this by implementing and using
    # getParentStyleInfo(style='blub') where parent styles are needed
    def inheritStyles(self, node, inheritStyle={}):
        """style information is handed down to child nodes."""

        def flattenStyle(styleHash):
            res =  {}
            for k,v in styleHash.items():
                if isinstance(v,dict):
                    for _k,_v in v.items():
                        if isinstance(_v, basestring):
                            res[_k.lower()] = _v.lower() 
                        else:
                            res[_k.lower()]= _v
                else:
                    if isinstance(v, basestring):
                        res[k.lower()] = v.lower() 
                    else:
                        res[k.lower()] = v
            return res

        def cleanInheritStyles(styleHash):
            sh = copy.copy(styleHash)
            ignoreStyles = ['border', 'border-spacing', 'background-color', 'background', 'class', 'margin', 'padding', 'align', 'colspan', 'rowspan',
                            'empty-cells', 'rules', 'clear', 'float', 'cellspacing', 'display', 'visibility']
            for style in ignoreStyles:
                sh.pop(style, None)
            return sh

        style = getattr(node, 'vlist', {})
        nodeStyle = inheritStyle
        if style:
            nodeStyle.update(flattenStyle(style))
            node.vlist = nodeStyle        
        elif inheritStyle:
            node.vlist = nodeStyle
        else:
            nodeStyle = {}

        for c in node.children:
            _is = cleanInheritStyles(nodeStyle)
            self.inheritStyles(c, inheritStyle=_is)


    def _getNext(self, node): #FIXME: name collides with advtree.getNext
        if not (node.next or node.parent):
            return
        next = node.next or node.parent.next
        if next and not next.isblocknode:
            if not next.getAllDisplayText().strip():
                return self._getNext(next)
        return next

    def _getPrev(self, node): #FIXME: name collides with advtree.getPrev(ious)
        if not (node.previous or node.parent):
            return
        prev = node.previous or node.parent 
        if prev and not prev.isblocknode:
            if not prev.getAllDisplayText().strip():
                return self._getPrev(prev)
        return prev

    def removeBreakingReturns(self, node): 
        """Remove BreakingReturns that occur around blocknodes or as the first/last element inside a blocknode."""
        if node.isblocknode:
            changed = True
            while changed:
                check_node = [node.getFirstLeaf(),
                             node.getLastLeaf(),
                             self._getNext(node),
                             self._getPrev(node)
                             ]
                changed = False
                for n in check_node:
                    if n.__class__ == BreakingReturn:
                        self.report('removing node', n)
                        tryRemoveNode(n)
                        changed = True

        for c in node.children:
            self.removeBreakingReturns(c)


    #FIXME: this method is used currently.
    # improve customization of treecleaner, b/c this method only needs to be used
    # by some writers: e.g. the ones that write footnotes should not need to print the ref-section
    def removeEmptyReferenceLists(self, node):
        """
        empty ReferenceLists are removed. they typically stick in a section which only contains the ReferenceList. That section is also removed
        """
        if node.__class__ == ReferenceList:
            removeNode = node
            while removeNode and (not removeNode.siblings or (removeNode.parent and removeNode.parent.__class__ == Section and len(removeNode.siblings) <= 1)):
                removeNode = removeNode.parent           
            if removeNode and removeNode.parent:
                self.report('removing node', removeNode)
                removeNode.parent.removeChild(removeNode)

        for c in node.children[:]:
            self.removeEmptyReferenceLists(c)


    def _fixParagraphs(self, node):
        """Move paragraphs to the child list of the last section (if existent)"""

        if isinstance(node, Paragraph) and isinstance(node.previous, Section) \
                and node.previous is not node.parent:
            prev = node.previous
            parent = node.parent
            target = prev.getLastChild()
            self.report('moving node', node, 'to', target)
            node.moveto(target)
            return True # changed
        else:
            for c in node.children[:]:
                if self._fixParagraphs(c):
                    return True

    def fixParagraphs(self, node):
        while self._fixParagraphs(node):
            pass

    def _nestingBroken(self, node):
        # FIXME: the list below is used and not node.isblocknode. is there a reason for that?
        blocknodes = (Paragraph, PreFormatted, ItemList, Section, Table,
                      Blockquote, DefinitionList, HorizontalRule, Source)
        parents = node.getParents()

        clean_parents = []
        parents.reverse()
        for p in parents:
            if p.__class__ not in self.outsideParentsInvisible:
                clean_parents.append(p)
            else:
                break
        clean_parents.reverse()
        parents = clean_parents

        if self.nesting_strictness == 'loose':
            for parent in parents:
                if parent.__class__ in self.forbidden_parents.get(node.__class__, []):
                    return parent
        elif self.nesting_strictness == 'strict':
            for parent in parents:
                if node.__class__ != Section and node.__class__ in blocknodes and parent.__class__ in blocknodes:
                    return parent
        return None

    def _buildSubTree(self, root, path, problem_node, side):
        if side == 'top':
            remove_children = False
            for c in root.children[:]:
                if remove_children or c == problem_node:
                    root.removeChild(c)
                if c in path:
                    remove_children= True
        elif side == 'bottom':
            remove_children = True
            for c in root.children[:]:
                if c in path:
                    remove_children= False
                if remove_children or c == problem_node:
                    root.removeChild(c)
        for c in root.children:
            self._buildSubTree(c, path, problem_node, side)

    def _buildMiddleTree(self, treestart, path2top, problem_node):        
        for c in treestart:
            if not c in path2top and c != problem_node and not problem_node in c.getParents():
                treestart.removeChild(c)
        for c in treestart:
            self._buildMiddleTree(c, path2top, problem_node)
            
    def _fixNesting(self, node):
        """Nesting of nodes is corrected.

        The strictness depends on nesting_strictness which can either be 'loose' or 'strict'.
        Depending on the strictness the _nestingBroken method uses different approaches to
        detect forbidden nesting.

        Example for 'strict' setting: (bn --> blocknode, nbn --> nonblocknode)
        bn_1
         nbn_2
         bn_3
         nbn_4

        becomes:
        bn_1.1
         nbn_2
        bn_3
        bn_1.2
         nbn_4
        """

        # EXPLANATION OF ALGORITHM:
        # 1. detect node (problem_child) with a parent that is forbidden (bad_parent)
        # split the tree starting from the forbidden parent into three parts.
        # middle path is the one leading from the first child of the bad_parent to the problem_child
        # left tree is copied from original, all nodes further right than the
        # path to the root node from the problem_child are remove
        # same for right tree

        bad_parent = self._nestingBroken(node)
        if bad_parent:
            path2root = node.getParents()
            problem_node = node
            root = bad_parent.parent
            path2root = path2root[path2root.index(root):]

            if bad_parent == node.parent: # direct nesting of problematic node and forbidden parent
                mtree = node                
                i = node.parent.children.index(node)
                if i > 0:
                    ttree = node.parent.copy()
                    ttree.children = ttree.children[:i]
                else:
                    ttree = None
                if i < len(node.parent.children):                    
                    btree = node.parent.copy()
                    btree.children = btree.children[i+1:]
                else:
                    btree = None
            else:
                ttree = bad_parent.copy()
                self._buildSubTree(ttree, path2root, problem_node, 'top')
                mtree = path2root[2].copy()
                self._buildMiddleTree(mtree, path2root, problem_node)
                btree = bad_parent.copy()
                self._buildSubTree(btree, path2root, problem_node, 'bottom')

            new_children = []
            if ttree:
                new_children.append(ttree)
            new_children.append(mtree)
            if btree:
                new_children.append(btree)                
            self.report('replacing child', bad_parent, 'by', new_children)
            root.replaceChild(bad_parent, new_children)
            return True
        else:
            for c in node.children:
                if self._fixNesting(c):
                    return True

        return False

    def fixNesting(self, node):
        while self._fixNesting(node):
            pass

   
    # ex: some tags need to be swapped: center nodes have to be pulled out of underline nodes
    # e.g. but only if the center is a direct and only child
    def swapNodes(self, node):
        """Swaps two nodes if nesting is problematic.

        Some writers have problems with some node combinations
        ex. <u><center>Text</center></u> --> <center><u>Text</u></center>
        """
        def swap(a,b): 
            assert len(a.children) == 1 and a.children[0] is b and b.parent is a and a.parent is not None
            ap = a.parent
            ap.replaceChild(a, [b])
            a.children = [] # a.removeChild(b) wouldn't work since check for b.parent which already is ap fails
            for c in b.children:
                a.appendChild(c)
            b.children = []
            b.appendChild(a)

        if node.__class__ in self.swapNodesMap:
            p = node.parent
            if p and p.parent and p.__class__ in self.swapNodesMap[node.__class__] and len(p.children) == 1:
                self.report('swapping nodes:', node.parent, node)
                swap(node.parent, node)

        for c in node.children[:]:
            self.swapNodes(c)

    def splitBigTableCells(self, node):
        """Splits table cells if their height exceeds the output page height.

        This method is only needed for writers that output on a paginated medium.
        Often these writers can not handle tables where a single cell exceeds the page height.
        Using heuristics in the treecleanerhelper.getNodeHeight function the height of a cell
        is estimated and the cell is split if necessary.        
        """      
        
        if node.__class__ == Row:
            for cell in node.children:
                h = getNodeHeight(cell, self.cell_splitter_params)
                if h > self.cell_splitter_params['maxCellHeight'] and len(cell.children) > 1:
                    rows = splitRow(node, self.cell_splitter_params)
                    self.report('replacing child', node, rows)
                    node.parent.replaceChild(node, rows)
                    return
            return

        for c in node.children[:]:
            self.splitBigTableCells(c)


    def removeNoPrintNodes(self, node):

        klasses = set(node.attributes.get('class', '').split())
        if set(self.noDisplayClasses).intersection(klasses) and node.parent:
            self.report('removing child', node)
            node.parent.removeChild(node)
            return

        for c in node.children[:]:
            self.removeNoPrintNodes(c)


    def cleanSectionCaptions(self, node):
        """Remove all block nodes from Section nodes, keep the content. If section title is empty replace section by br node"""
        
        if node.__class__ == Section:
            assert node.children, 'Error, section has no children'
            assert node.parent, 'Error, section has no parents'
            if not node.children[0].children:
                children = [BreakingReturn()]
                if len(node.children) > 1: # at least one "content" node
                    children.extend(node.children)
                self.report('replaced section with empty title with br node')
                node.parent.replaceChild(node, children)
    
        if node.__class__ == Section:
            caption_node = node.children[0]
            children = caption_node.getAllChildren()
            for c in children:
                if c.isblocknode:
                    self.report('removed block node', c)
                    c.parent.replaceChild(c, c.children)

        for c in node.children[:]:
            self.cleanSectionCaptions(c)
            

    def findDefinitionLists(self, node):
        if node.__class__ in [DefinitionTerm, DefinitionDescription]:
            prev = node.getPrevious()
            parent = node.getParent()
            if prev.__class__ == DefinitionList: 
                node.moveto(prev.getLastChild())
            else: 
                dl = DefinitionList()
                parent.replaceChild(node, [dl])
                dl.appendChild(node)

        for c in node.children[:]:
            self.findDefinitionLists(c)
