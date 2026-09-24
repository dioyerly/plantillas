class Navigation:
    """Registry records intent separately from PDF annotations for validation."""
    def __init__(self, pages):
        self.pages = {p['id']: i for i,p in enumerate(pages)}
        if len(self.pages) != len(pages):
            raise ValueError('Duplicate page IDs')
        self.destinations = {k: {'page':v, 'fit':'Fit'} for k,v in self.pages.items()}
        self.links = []

    def anchor(self, canvas, key, page_id, bounds):
        if key in self.destinations:
            raise ValueError(f'Duplicate destination: {key}')
        x,y,w,h = bounds
        from .config import HEIGHT
        canvas.bookmarkPage(key, fit='FitR', left=x, bottom=HEIGHT-y-h, right=x+w, top=HEIGHT-y)
        self.destinations[key] = {'page':self.pages[page_id], 'fit':'FitR', 'bounds':list(bounds)}

    def link(self, canvas, source, target, label, bounds):
        return self._link(canvas, source, target, label, bounds, True)

    def link_small(self, canvas, source, target, label, bounds):
        """Create a compact calendar-cell link; touch area is the printed date cell."""
        return self._link(canvas, source, target, label, bounds, False)

    def _link(self, canvas, source, target, label, bounds, enforce_target):
        from .config import HEIGHT, MIN_TARGET
        x,y,w,h = bounds
        if enforce_target:
            assert w >= MIN_TARGET and h >= MIN_TARGET, (label,w,h)
        canvas.linkAbsolute(label, target, Rect=(x,HEIGHT-y-h,x+w,HEIGHT-y), thickness=0)
        self.links.append({'source':self.pages[source], 'target':target, 'label':label, 'bounds':list(bounds)})

    def check(self):
        for link in self.links:
            assert link['target'] in self.destinations, link
        reached = {0}
        while True:
            expanded = reached | {self.destinations[x['target']]['page'] for x in self.links if x['source'] in reached}
            if expanded == reached:
                break
            reached = expanded
        assert reached == set(self.pages.values()), ('Unreachable pages',set(self.pages.values())-reached)
