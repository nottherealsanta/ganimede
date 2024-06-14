export let path = "test_nb.ipynb";
export let cell_ids = [
    "JiXjY973",
    "U2dG4mjD",
    "CmdY3sdw",
    "Q2dG4mjD",
    "F9j3Bj2o",
    "H93BfwI8",
    "jBu3Ivjd"
  ];
export let cell_maps : {[key: string]: any} = {
  "JiXjY973": {
    "id": "JiXjY973",
    "type": "python",
    "source": ["print('Hello world')"],
    "execution_count": 1,
    "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Hello World\n"
     ]
    }
   ],
    "heading_level": null,
    "collapsed": false,
    "parent_collapsed": false,
    "state": "idle",
    "execution_time": 0.1
  },
  "U2dG4mjD": {
    "id": "U2dG4mjD",
    "type": "markdown",
    "source": [
     "# This is a heading 1"
    ],
    "heading_level": 1,
    "collapsed": false,
    "parent_collapsed": false,
    "state": "idle",
    "execution_time": null
   },
  "CmdY3sdw": {
    "id": "CmdY3sdw",
    "type": "python",
    "source": [
    "import numpy as np\n",
    "import scipy.sparse as sp\n",
    "import waves\n",
    "import matplotlib.pyplot as plt\n",
    "import skimage.io as io\n",
    "import scipy.ndimage.filters as filters\n",
    "import matplotlib.animation as animation"
   ],
    "execution_count": 2,
    "outputs": [],
    "heading_level": null,
    "collapsed": false,
    "parent_collapsed": false,
    "state": "idle",
    "execution_time": 0.5
  },
  "Q2dG4mjD": {
    "id": "Q2dG4mjD",
    "type": "markdown",
    "source": [
     "This is a markdown cell"
    ],
    "heading_level": null,
    "collapsed": false,
    "parent_collapsed": false,
    "state": "idle",
    "execution_time": null
  },
  "F9j3Bj2o": {
    "id": "F9j3Bj2o",
    "type": "sql",
    "source": [
      "SELECT * FROM table\n",
      "WHERE column = 'value'\n",
      "ORDER BY column\n",
      "LIMIT 10"
    ],
    "heading_level": null,
    "collapsed": false,
    "parent_collapsed": false,
    "state": "idle",
    "execution_time": null
  },
  "H93BfwI8": {
    "id": "H93BfwI8",
    "type": "markdown",
    "source": [
     "# This also is a heading 1\n",
      "This is some text in the markdown cell"
    ],
    "heading_level": 1,
    "collapsed": false,
    "parent_collapsed": false,
    "state": "idle",
    "execution_time": null
   },
   "jBu3Ivjd": {
    "id": "jBu3Ivjd",
    "type": "python",
    "source": [
    "a = np.array([1, 2, 3, 4, 5])\n",
    "b = np.array([6, 7, 8, 9, 10])\n",
    "c = a + b\n",
    "print(c)"
   ],
    "execution_count": 4,
    "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "[ 7  9 11 13 15]\n"
     ]
    }
    ],
    "heading_level": null,
    "collapsed": false,
    "parent_collapsed": false,
    "state": "idle",
    "execution_time": 0.5
  },
}