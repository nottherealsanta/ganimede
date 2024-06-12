export let path = "test_nb.ipynb";
export let cell_ids = [
    "JiXjY973",
    "U2dG4mjD",
    "CmdY3sdw",
    "Q2dG4mjD",
  ];
export let cell_maps : {[key: string]: any} = {
  "JiXjY973": {
    "id": "JiXjY973",
    "type": "code",
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
    "type": "code",
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
  }
}